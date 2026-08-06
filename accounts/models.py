from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='')
    telefone = models.CharField(max_length=11)
    cargo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    imagem = models.ImageField(upload_to='perfis/', blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    