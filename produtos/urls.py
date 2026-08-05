from django.urls import path
from . import views

urlpatterns = [
    path('', views.produto_list_view, name='produto_list'),
    path('novo/', views.produto_create, name='produto_create'),
    path('<int:pk>/', views.produto_detail_view, name='produto_detail'),
    path('<int:pk>/editar/', views.produto_update_view, name='produto_update'),
    path('<int:pk>/excluir/', views.produto_delete, name='produto_delete'),
]