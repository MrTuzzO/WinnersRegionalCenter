from docs.models import RequiredDocument, UserDocument

def is_all_steps_completed(user):
    total = RequiredDocument.objects.count()
    if total == 0:
        return False
    approved = UserDocument.objects.filter(user=user, status='approved').count()
    return approved == total