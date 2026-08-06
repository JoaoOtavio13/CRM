from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nome')

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('nome', 'telefone', 'cargo', 'cpf', 'empresa', 'imagem')
