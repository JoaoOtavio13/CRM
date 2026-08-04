from django.shortcuts import redirect, render

from produtos.forms import ProdutoForm
from .models import Produto

# Create your views here.
def ProdutoListView(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/produto_list.html', {'produtos': produtos})

def ProdutoDetailView(request, pk):
    produto = Produto.objects.get(pk=pk)
    return render(request, 'produtos/produto_detail.html', {'produto': produto})

def ProdutoUpdateView(request, pk):
    produto = Produto.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/produto_form.html', {'form': form})

def Produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm()
    return render(request, 'produtos/produto_form.html', {'form': form})

def Produto_delete(request, pk):
    produto = Produto.objects.get(pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'produtos/produto_confirm_delete.html', {'produto': produto})