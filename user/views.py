from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from core.response import success_response, error_response
from .models import OTP, User
from .serializers import *
from .utils import send_otp_email
from user.permission import IsAdmin
from rest_framework import viewsets
# for Api documentation
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer

class Users(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_email_verified', 'is_staff']
    search_fields = ['email', 'name']
    ordering_fields = ['created_at']
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserListSerializer
        return UserDetailSerializer

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     @extend_schema(request=RegisterSerializer, responses={201: OpenApiTypes.OBJECT})
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {"detail": "Registration successful. Please check your email for the verification OTP."},
#             status=status.HTTP_201_CREATED,
#         )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=VerifyEmailSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        otp_obj = serializer.validated_data["otp_obj"]

        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return success_response("Email verified successfully.", status.HTTP_200_OK)


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ResendOTPSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        purpose = serializer.validated_data["purpose"]
        send_otp_email(user, purpose)

        return success_response("OTP sent successfully.", status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return success_response(
            "Login successful.",
            status.HTTP_200_OK,
            data={
                "access": data["access"],
                "refresh": data["refresh"],
                "user": UserProfileSerializer(data["user"]).data,
            },
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=inline_serializer(
        name="LogoutRequest",
        fields={
            "refresh": OpenApiTypes.STR,
        },
    ), responses={200: OpenApiTypes.OBJECT})

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return error_response(
                "Request failed",
                status.HTTP_400_BAD_REQUEST,
                errors={"detail": "Refresh token is required."},
            )
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return error_response(
                "Request failed",
                status.HTTP_400_BAD_REQUEST,
                errors={"detail": "Invalid or already-expired token."},
            )
        return success_response("Logged out successfully.", status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserProfileSerializer})
    def get(self, request):
        return success_response(
            "Profile fetched successfully.",
            status.HTTP_200_OK,
            data=UserProfileSerializer(request.user).data,
        )

    @extend_schema(request=UserProfileSerializer, responses={200: UserProfileSerializer})    
    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            "Profile updated successfully.",
            status.HTTP_200_OK,
            data=serializer.data,
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return success_response("Password changed successfully.", status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ForgotPasswordSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
            send_otp_email(user, OTP.PURPOSE_PASSWORD_RESET)
        except User.DoesNotExist:
            pass  # silently ignore – prevent user enumeration

        return success_response(
            "If an account with that email exists, a password reset OTP has been sent.",
            status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ResetPasswordSerializer, responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        otp_obj = serializer.validated_data["otp_obj"]

        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return success_response(
            "Password reset successfully. You can now log in.",
            status.HTTP_200_OK,
        )
