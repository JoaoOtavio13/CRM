from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
            Perfil.objects.create(
                user=user,
                nome=form.cleaned_data['nome'],
                telefone=form.cleaned_data.get('telefone', ''),
                cargo=form.cleaned_data.get('cargo', ''),
                cpf=form.cleaned_data.get('cpf', ''),
                empresa=form.cleaned_data.get('empresa', ''),
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