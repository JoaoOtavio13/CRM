from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'descricao', 'preco', 'estoque', 'data_criacao', 'data_atualizacao')
    search_fields = ('nome', 'descricao')
    list_filter = ('usuario', 'data_criacao', 'data_atualizacao')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')