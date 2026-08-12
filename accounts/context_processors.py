from .models import Admin


def is_admin_context(request):
    """
    Context processor que disponibiliza 'is_admin' para todos os templates.
    """
    if not request.user.is_authenticated:
        return {'is_admin': False}

    is_admin = request.user.is_superuser or Admin.objects.filter(user=request.user).exists()
    return {'is_admin': is_admin}