from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Processa a empresa (cria se não existir)
            nome_empresa = form.cleaned_data.get('empresa_nome', '').strip()
            empresa = None
            if nome_empresa:
                empresa, created = Empresa.objects.get_or_create(
                    nome=nome_empresa,
                    defaults={
                        'cnpj': form.cleaned_data.get('cnpj', ''),
                        'endereco': form.cleaned_data.get('endereco', ''),
                        'telefone': form.cleaned_data.get('telefone_empresa', ''),
                        'email': form.cleaned_data.get('email_empresa', ''),
                    },
                )

            # Cria o perfil vinculado ao usuário
            Perfil.objects.create(
                user=user,
                nome=form.cleaned_data['nome'],
                telefone=form.cleaned_data.get('telefone', ''),
                cargo=form.cleaned_data.get('cargo', ''),
                cpf=form.cleaned_data.get('cpf', ''),
                empresa=empresa,
                imagem=form.cleaned_data.get('imagem'),
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def perfil(request):
    user = request.user
    Perfil.objects.get_or_create(user=user)
    context = {'user': user,}
    return render(request, 'accounts/perfil.html', context)

@login_required
def editar_perfil(request):
    user = request.user
    perfil, created = Perfil.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'accounts/editar_perfil.html', {'form': form})

@login_required
def deletar_perfil(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Perfil deletado com sucesso.')
        return redirect('index')
    return render(request, 'accounts/deletar_perfil.html', {'user': user})

def redefinir_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[uid, token])
            )
            send_mail(
                'Redefinição de Senha',
                f'Olá {user.username},\n\n'
                f'Recebemos uma solicitação para redefinir sua senha.\n\n'
                f'Clique no link abaixo para redefinir sua senha:\n'
                f'{link}\n\n'
                f'Se você não solicitou esta alteração, ignore este e-mail.\n\n'
                f'Atenciosamente,\nEquipe Vendas CRM',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            messages.success(request, 'Um e-mail de redefinição de senha foi enviado.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Nenhum usuário encontrado com este e-mail.')
    return render(request, 'accounts/redefinir_senha.html')

def nova_senha(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            nova_senha = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')
            if nova_senha and nova_senha == confirmar_senha:
                user.set_password(nova_senha)
                user.save()
                messages.success(request, 'Senha redefinida com sucesso. Faça login.')
                return redirect('login')
            else:
                messages.error(request, 'As senhas não coincidem ou estão vazias.')
        return render(request, 'accounts/nova_senha.html', {'validlink': True})
    return render(request, 'accounts/nova_senha.html', {'validlink': False})

@login_required
def empresa_list(request):
    empresas = Empresa.objects.all()
    return render(request, 'accounts/empresa_list.html', {'empresas': empresas})

@login_required
def empresa_create(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empresa_list')
    else:
        form = EmpresaForm()
    return render(request, 'accounts/empresa_form.html', {'form': form})

@login_required
def empresa_update(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('empresa_list')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'accounts/empresa_form.html', {'form': form})

@login_required
def empresa_delete(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        return redirect('empresa_list')
    return render(request, 'accounts/empresa_confirm_delete.html', {'empresa': empresa})