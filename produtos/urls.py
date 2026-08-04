from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProdutoListView, name='produto_list'),
    path('novo/', views.Produto_create, name='produto_create'),
    path('<int:pk>/', views.ProdutoDetailView, name='produto_detail'),
    path('<int:pk>/editar/', views.ProdutoUpdateView, name='produto_update'),
    path('<int:pk>/excluir/', views.Produto_delete, name='produto_delete'),
]