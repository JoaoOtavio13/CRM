from django.conf import settings
from django.db import models

# Create your models here.

class Empresa(models.Model):
	nome = models.CharField(max_length=120)
	dono = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empresa')

	def __str__(self):
		return self.nome
