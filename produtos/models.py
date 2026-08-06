from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

User = get_user_model()

class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produtos', null=True, blank=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.estoque is not None and self.estoque < 0:
            raise ValidationError({'estoque': 'O estoque não pode ser negativo.'})

    def baixar_estoque(self, quantidade):
        if quantidade <= 0:
            raise ValidationError({'estoque': 'A quantidade deve ser maior que zero.'})
        if self.estoque < quantidade:
            raise ValidationError({'estoque': 'Estoque insuficiente para realizar a venda.'})
        self.estoque -= quantidade
        self.save(update_fields=['estoque', 'data_atualizacao'])

    def repor_estoque(self, quantidade):
        if quantidade <= 0:
            raise ValidationError({'estoque': 'A quantidade deve ser maior que zero.'})
        self.estoque += quantidade
        self.save(update_fields=['estoque', 'data_atualizacao'])

    def __str__(self):
        return self.nome