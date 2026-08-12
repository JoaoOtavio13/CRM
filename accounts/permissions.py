from rest_framework.permissions import BasePermission

from .models import Admin


class IsEmpresaAdmin(BasePermission):
    """
    Permite acesso somente ao usuário que é administrador da empresa.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return Admin.objects.filter(user=request.user).exists()
