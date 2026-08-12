from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendas_list, name='vendas_list'),
    path('nova/', views.registrar_venda, name='registrar_venda'),
    path('<int:pk>/', views.venda_detail, name='venda_detail'),
    path('<int:pk>/excluir/', views.venda_delete, name='venda_delete'),
    path('faturamento/', views.faturamento, name='faturamento'),
    path('clientes/', views.listar_clientes, name='clientes_list'),
    path('clientes/cadastro/', views.cadastro_cliente, name='cadastro_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/excluir/', views.deletar_cliente, name='deletar_cliente'),
]