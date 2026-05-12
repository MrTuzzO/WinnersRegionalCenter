from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RequiredDocument, UserDocument
from user.permission import IsAdmin
from .serializers import *

User = get_user_model()


def _safe_file_url(value, request=None):
    if not value:
        return ''
    try:
        url = value.url
    except Exception:
        name = getattr(value, 'name', '')
        if isinstance(name, bytes):
            name = name.decode('utf-8', errors='replace')
        url = str(name)

    if request is not None and isinstance(url, str) and url.startswith('/'):
        try:
            return request.build_absolute_uri(url)
        except Exception:
            pass
    return url


def get_user_progress_data(user, request=None):
    required_docs = list(RequiredDocument.objects.order_by('step'))
    total_steps = len(required_docs)
    user_docs_qs = UserDocument.objects.filter(user=user).select_related('required_document')
    user_docs_by_required_id = {obj.required_document_id: obj for obj in user_docs_qs}

    completed_documents = []
    current_document = None

    for req_doc in required_docs:
        user_doc = user_docs_by_required_id.get(req_doc.id)

        if user_doc and user_doc.status == 'approved':
            completed_documents.append(
                {
                    'user_document_id': user_doc.id,
                    'required_document_id': req_doc.id,
                    'step': req_doc.step,
                    'title': req_doc.title,
                    'download_file': _safe_file_url(req_doc.file, request),
                    'signed_file': _safe_file_url(user_doc.signed_file, request),
                    'status': user_doc.status,
                    'reviewed_at': user_doc.reviewed_at,
                }
            )
            continue

        current_document = {
            'user_document_id': user_doc.id if user_doc else None,
            'required_document_id': req_doc.id,
            'step': req_doc.step,
            'title': req_doc.title,
            'download_file': _safe_file_url(req_doc.file, request),
            'signed_file': _safe_file_url(user_doc.signed_file, request) if user_doc else None,
            'status': user_doc.status if user_doc else 'not_started',
            'admin_note': user_doc.admin_note if user_doc else '',
            'submitted_at': user_doc.submitted_at if user_doc else None,
            'reviewed_at': user_doc.reviewed_at if user_doc else None,
            'allow_upload': not user_doc or user_doc.status == 'rejected',
        }
        break

    all_completed = total_steps > 0 and current_document is None

    return {
        'total_steps': total_steps,
        'completed_steps': len(completed_documents),
        'all_completed': all_completed,
        'current_step': current_document['step'] if current_document else None,
        'completed_documents': completed_documents,
        'current_document': current_document,
    }


@extend_schema_view(
    get=extend_schema(
        summary='User workflow progress',
        description='Returns total steps, approved forms, and only one current step. Next step is hidden until admin approval.',
        responses={'200': UserProgressSerializer},
    )
)
class UserProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        progress = get_user_progress_data(request.user, request)
        if progress['total_steps'] == 0:
            return Response({'detail': 'No required documents configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(progress)


@extend_schema_view(
    post=extend_schema(
        summary='Upload signed file for current step',
        description='Uploads for the current step only. User cannot upload any future step before approval.',
        request=UploadStepSerializer,
        responses={'200': UserProgressSerializer},
    )
)
class UserUploadCurrentStepView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        progress = get_user_progress_data(request.user, request)
        if progress['total_steps'] == 0:
            return Response({'detail': 'No required documents configured yet.'}, status=status.HTTP_404_NOT_FOUND)
        if progress['all_completed']:
            return Response({'detail': 'All steps are already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        current = progress['current_document']
        if not current:
            return Response({'detail': 'No active step found.'}, status=status.HTTP_400_BAD_REQUEST)
        if not current['allow_upload']:
            return Response({'detail': 'Current step already submitted. Wait for admin review.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UploadStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        req_doc = generics.get_object_or_404(RequiredDocument, pk=current['required_document_id'])
        user_doc = UserDocument.objects.filter(user=request.user, required_document=req_doc).first()

        if user_doc:
            user_doc.signed_file = serializer.validated_data['signed_file']
            user_doc.status = 'submitted'
            user_doc.admin_note = ''
            user_doc.reviewed_at = None
            user_doc.submitted_at = timezone.now()
            user_doc.save(update_fields=['signed_file', 'status', 'admin_note', 'reviewed_at', 'submitted_at'])
        else:
            UserDocument.objects.create(
                user=request.user,
                required_document=req_doc,
                signed_file=serializer.validated_data['signed_file'],
                status='submitted',
            )

        return Response(get_user_progress_data(request.user, request), status=status.HTTP_200_OK)


# ── Admin ─────────────────────────────────────────────────────────────────

class AdminRequiredDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = AdminRequiredDocumentSerializer
    permission_classes = [IsAdmin]
    queryset = RequiredDocument.objects.all()


@extend_schema_view(
    get=extend_schema(
        summary='Admin: users with current step status',
        description='Table view: one row per user showing name, email, current step, progress.',
        responses={'200': AdminUserStepListSerializer(many=True)},
    )
)
class AdminUserStepListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminUserStepListSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=False).order_by('id')

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        rows = []
        for user in users:
            progress = get_user_progress_data(user, request)
            status_label = 'Completed' if progress['all_completed'] else (f"Step {progress['current_step']}" if progress['current_step'] else 'Pending')
            rows.append({
                'user_id': user.id,
                'user_name': user.name,
                'user_email': user.email,
                'completed_steps': progress['completed_steps'],
                'current_step': progress['current_step'],
                'status_label': status_label,
            })
        return Response(rows)


@extend_schema_view(
    get=extend_schema(
        summary='Admin: user all steps detail',
        description='Detail view: all steps for one user (completed + current + locked future).',
        responses={'200': AdminUserStepDetailSerializer},
    )
)
class AdminUserStepDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, user_id):
        user = generics.get_object_or_404(User, pk=user_id)
        progress = get_user_progress_data(user, request)
        submitted_qs = UserDocument.objects.filter(user=user).select_related('user', 'required_document').order_by(
            'required_document__step', '-submitted_at'
        )
        data = {
            'user_id': user.id,
            'user_name': user.name,
            'user_email': user.email,
            'total_steps': progress['total_steps'],
            'current_step': progress['current_step'],
            'submitted_documents': AdminSubmissionSerializer(submitted_qs, many=True, context={'request': request}).data,
        }
        return Response(data)


@extend_schema(
    summary='Review submission (admin)',
    description='Approve or reject one submitted document.',
    request=AdminReviewSerializer,
    responses={'200': AdminSubmissionSerializer},
    methods=['PATCH'],
)
class AdminReviewView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        user_doc = generics.get_object_or_404(UserDocument, pk=pk)
        if user_doc.status != 'submitted':
            return Response({'detail': 'Only submitted documents can be reviewed.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdminReviewSerializer(user_doc, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewed_at=timezone.now())

        return Response(AdminSubmissionSerializer(user_doc, context={'request': request}).data, status=status.HTTP_200_OK)
