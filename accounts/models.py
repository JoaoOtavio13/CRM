from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, default='')
    telefone = models.CharField(max_length=11)
    cargo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    imagem = models.ImageField(upload_to='perfis/', blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='perfis', null=True, blank=True)
    