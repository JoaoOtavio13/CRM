import hashlib

from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


def buscar_ou_criar_empresa(nome):
    """
    Busca uma empresa pelo nome (case-insensitive, sem espaços extras).
    Se não existir, cria uma nova com CNPJ único gerado via hash.
    Retorna a empresa encontrada ou criada.
    """
    nome = nome.strip()
    if not nome:
        return None

    # Busca case-insensitive para evitar duplicatas
    empresa = Empresa.objects.filter(nome__iexact=nome).first()
    if not empresa:
        cnpj = hashlib.md5(nome.encode()).hexdigest()[:14]
        empresa = Empresa.objects.create(nome=nome, cnpj=cnpj)
    return empresa


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Campos do Perfil
    nome = forms.CharField(max_length=100, required=True)
    telefone = forms.CharField(max_length=11, required=False)
    cargo = forms.CharField(max_length=100, required=False)
    cpf = forms.CharField(max_length=11, required=False)
    imagem = forms.ImageField(required=False)

    # Campos da Empresa
    empresa_nome = forms.CharField(max_length=100, required=True, help_text='Digite o nome da empresa. Se ela não existir, será criada automaticamente.')
    cnpj = forms.CharField(max_length=14, required=False, help_text='CNPJ da empresa (apenas números).')
    endereco = forms.CharField(max_length=255, required=False)
    telefone_empresa = forms.CharField(max_length=11, required=False)
    email_empresa = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nome', 'telefone', 'cargo', 'cpf', 'imagem',
                  'empresa_nome', 'cnpj', 'endereco', 'telefone_empresa', 'email_empresa')


class PerfilForm(forms.ModelForm):
    empresa_nome = forms.CharField(
        max_length=100,
        required=True,
        help_text='Digite o nome da empresa. Se ela não existir, será criada automaticamente.'
    )

    class Meta:
        model = Perfil
        fields = ('nome', 'telefone', 'cargo', 'cpf', 'imagem')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.empresa:
            self.fields['empresa_nome'].initial = self.instance.empresa.nome

    def save(self, commit=True):
        perfil = super().save(commit=False)
        nome_empresa = self.cleaned_data.get('empresa_nome', '').strip()
        if nome_empresa:
            perfil.empresa = buscar_ou_criar_empresa(nome_empresa)
        if commit:
            perfil.save()
        return perfil

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ('nome', 'cnpj', 'endereco', 'telefone', 'email')


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('user', 'empresa')
