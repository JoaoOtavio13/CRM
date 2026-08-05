from django.shortcuts import render, redirect, get_object_or_404
from .models import Venda
from .forms import VendaForm


def registrar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save()
            return redirect('venda_detail', pk=venda.pk)
    else:
        form = VendaForm()
    return render(request, 'vendas/registrar_venda.html', {'form': form})


def vendas_list(request):
    vendas = Venda.objects.all()
    return render(request, 'vendas/vendas_list.html', {'vendas': vendas})


def venda_detail(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'vendas/venda_detail.html', {'venda': venda})


def venda_delete(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        venda.delete()
        return redirect('vendas_list')
    return render(request, 'vendas/venda_confirm_delete.html', {'venda': venda})