from django.contrib import admin
from .models import Produto

# Register your models here.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'descricao', 'preco', 'estoque', 'data_criacao', 'data_atualizacao')
    search_fields = ('nome', 'descricao')
    list_filter = ('usuario', 'data_criacao', 'data_atualizacao')
