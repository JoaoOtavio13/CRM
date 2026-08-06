from rest_framework import serializers
from .models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco', 'estoque', 'imagem', 'data_criacao', 'data_atualizacao')
        read_only_fields = ('id', 'data_criacao', 'data_atualizacao')

    def validate_estoque(self, value):
        if value < 0:
            raise serializers.ValidationError('O estoque não pode ser negativo.')
        return value

    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError('O preço deve ser maior que zero.')
        return value