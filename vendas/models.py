from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum
from produtos.models import Produto
# Create your models here.
class Venda(models.Model):
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))

    def atualizar_total(self):
        total = self.itens.aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')
        if self.total != total:
            self.total = total
            super().save(update_fields=['total'])

    def save(self, *args, **kwargs):
        if self.pk is None and self.total is None:
            self.total = Decimal('0.00')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            for item in self.itens.select_related('produto').all():
                produto = Produto.objects.select_for_update().get(pk=item.produto_id)
                produto.repor_estoque(item.quantidade)
            super().delete(*args, **kwargs)


    def __str__(self):
        return f"Venda #{self.pk or 'nova'} em {self.data_venda}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('produtos.Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if self.quantidade <= 0:
            raise ValidationError({'quantidade': 'A quantidade deve ser maior que zero.'})

        with transaction.atomic():
            produto = Produto.objects.select_for_update().get(pk=self.produto_id)
            item_antigo = None

            if self.pk:
                item_antigo = ItemVenda.objects.select_for_update().get(pk=self.pk)

            if item_antigo is not None:
                if item_antigo.produto_id == produto.pk:
                    diferenca = self.quantidade - item_antigo.quantidade
                    if diferenca > 0:
                        produto.baixar_estoque(diferenca)
                    elif diferenca < 0:
                        produto.repor_estoque(abs(diferenca))
                else:
                    item_antigo.produto.repor_estoque(item_antigo.quantidade)
                    produto.baixar_estoque(self.quantidade)
            else:
                produto.baixar_estoque(self.quantidade)

            self.subtotal = Decimal(produto.preco) * self.quantidade
            self.produto = produto
            super().save(*args, **kwargs)
            self.venda.atualizar_total()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            produto = Produto.objects.select_for_update().get(pk=self.produto_id)
            produto.repor_estoque(self.quantidade)
            venda = self.venda
            super().delete(*args, **kwargs)
            venda.atualizar_total()

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"

