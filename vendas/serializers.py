from rest_framework import serializers
from .models import Venda, ItemVenda
from produtos.models import Produto
from produtos.serializers import ProdutoSerializer


class ItemVendaSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all(),
        source='produto',
        write_only=True
    )

    class Meta:
        model = ItemVenda
        fields = ('id', 'produto', 'produto_id', 'quantidade', 'subtotal')
        read_only_fields = ('id', 'subtotal')


class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True, default=None)

    class Meta:
        model = Venda
        fields = ('id', 'numero', 'usuario', 'data_venda', 'total', 'cliente', 'cliente_nome', 'itens')
        read_only_fields = ('id', 'numero', 'usuario', 'data_venda', 'total')
