from django.shortcuts import redirect, render, get_object_or_404

from produtos.forms import ProdutoForm
from .models import Produto


def produto_list_view(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/produto_list.html', {'produtos': produtos})


def produto_detail_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produtos/produto_detail.html', {'produto': produto})


def produto_update_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/produto_form.html', {'form': form})


def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm()
    return render(request, 'produtos/produto_form.html', {'form': form})


def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'produtos/produto_confirm_delete.html', {'produto': produto})