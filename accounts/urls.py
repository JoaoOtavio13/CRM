from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/deletar/', views.deletar_perfil, name='deletar_perfil'),
    path('redefinir-senha/', views.redefinir_senha, name='password_reset'),
    path('redefinir-senha/<uidb64>/<token>/', views.nova_senha, name='password_reset_confirm'),
    path('empresas/', views.empresa_list, name='empresa_list'),
    path('empresas/nova/', views.empresa_create, name='empresa_create'),
    path('empresas/<int:pk>/editar/', views.empresa_update, name='empresa_update'),
    path('empresas/<int:pk>/excluir/', views.empresa_delete, name='empresa_delete'),
]
