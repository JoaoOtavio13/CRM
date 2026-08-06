from rest_framework import viewsets, permissions
from .models import Produto
from .serializers import ProdutoSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de produtos.
    Apenas usuários autenticados podem acessar.
    Cada usuário só vê e gerencia seus próprios produtos.
    """
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Produto.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)