from django.urls import path
from . import views

urlpatterns = [
    path('', views.produto_list_view, name='produto_list'),
    path('novo/', views.produto_create, name='produto_create'),
    path('<int:pk>/', views.produto_detail_view, name='produto_detail'),
    path('<int:pk>/editar/', views.produto_update_view, name='produto_update'),
    path('<int:pk>/excluir/', views.produto_delete, name='produto_delete'),
    path('categorias/', views.categoria_list_view, name='categoria_list'),
    path('categorias/novo/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update_view, name='editar_categoria'),
    path('categorias/<int:pk>/excluir/', views.categoria_delete, name='categoria_delete'),
]