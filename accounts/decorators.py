from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Admin


def admin_required(view_func):
    """
    Decorator que permite acesso apenas a usuários que são admin
    (superuser ou registrado no modelo Admin).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_superuser or Admin.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Acesso restrito. Apenas administradores podem acessar esta página.')
        return redirect('index')

    return _wrapped_view