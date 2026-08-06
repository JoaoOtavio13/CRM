from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'cliente', 'data_venda', 'total')
    list_filter = ('data_venda', 'usuario', 'cliente')
    search_fields = ('usuario__username', 'cliente__nome')

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'produto', 'quantidade', 'subtotal')
    search_fields = ('produto__nome',)
    list_filter = ('venda__data_venda',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'usuario')
    search_fields = ('nome', 'email')
    list_filter = ('usuario',)
