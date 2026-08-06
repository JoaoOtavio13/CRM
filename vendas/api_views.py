from decimal import Decimal
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Venda
from .serializers import VendaSerializer


class FaturamentoAPIView(APIView):
    """
    Endpoint para listar o faturamento do usuário logado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendas = Venda.objects.filter(usuario=request.user)
        total_faturamento = sum((venda.total for venda in vendas), Decimal('0.00'))

        return Response({
            'usuario': request.user.username,
            'total_faturamento': str(total_faturamento),
            'total_vendas': vendas.count(),
        }, status=status.HTTP_200_OK)


class VendaListAPIView(APIView):
    """
    Endpoint para listar as vendas do usuário logado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendas = Venda.objects.filter(usuario=request.user)
        serializer = VendaSerializer(vendas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)