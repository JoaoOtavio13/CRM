from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quantidade', 'data_venda', 'total')
    search_fields = ('produto__nome',)
    list_filter = ('data_venda',)

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'produto', 'quantidade', 'preco_unitario')
    search_fields = ('produto__nome',)
    list_filter = ('venda__data_venda',)
