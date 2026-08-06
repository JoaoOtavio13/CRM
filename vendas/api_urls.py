from django.urls import path
from .api_views import FaturamentoAPIView, VendaListAPIView

urlpatterns = [
    path('faturamento/', FaturamentoAPIView.as_view(), name='api_faturamento'),
    path('vendas/', VendaListAPIView.as_view(), name='api_vendas_list'),
]