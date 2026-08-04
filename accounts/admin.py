from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone', 'cargo', 'cpf', 'imagem')