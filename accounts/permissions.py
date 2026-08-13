from rest_framework.permissions import BasePermission

from .models import Admin


class IsEmpresaAdmin(BasePermission):
    """
    Permite acesso somente ao usuário que é administrador da empresa
    vinculada ao seu perfil (o dono da empresa).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # Empresa vinculada ao perfil do usuário logado
        perfil = getattr(request.user, 'perfil', None)
        if perfil is None or perfil.empresa_id is None:
            return False

        # Verifica se o usuário é admin (dono) dessa empresa específica
        return Admin.objects.filter(
            user=request.user,
            empresa_id=perfil.empresa_id,
        ).exists()
