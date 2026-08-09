from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from produtos.forms import ProdutoForm
from .models import *


@login_required
def produto_list_view(request):
    produtos = Produto.objects.filter(usuario=request.user)
    return render(request, 'produtos/produto_list.html', {'produtos': produtos})


@login_required
def produto_detail_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk, usuario=request.user)
    return render(request, 'produtos/produto_detail.html', {'produto': produto})


@login_required
def produto_update_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/produto_form.html', {'form': form})


@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.usuario = request.user
            produto.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm()
    return render(request, 'produtos/produto_form.html', {'form': form})


@login_required
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'produtos/produto_confirm_delete.html', {'produto': produto})

@login_required
def categoria_list_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        categoria = Categoria(nome=nome, descricao=descricao)
        categoria.save()
        return redirect('categoria_list')
    return render(request, 'produtos/categoria_form.html')

@login_required
def categoria_update_view(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.descricao = request.POST.get('descricao')
        categoria.save()
        return redirect('categoria_list')
    return render(request, 'produtos/categoria_form.html', {'categoria': categoria})

@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
    return render(request, 'produtos/categoria_confirm_delete.html', {'categoria': categoria})