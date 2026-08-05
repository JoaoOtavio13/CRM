from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Empresa
from .models import Venda
from .forms import ItemVendaFormSet


@login_required
def registrar_venda(request):
    if request.method == 'POST':
        venda = Venda()
        formset = ItemVendaFormSet(request.POST, instance=venda)
        if formset.is_valid():
            with transaction.atomic():
                venda.save()
                formset.instance = venda
                formset.save()
                venda.refresh_from_db()
            return redirect('venda_detail', pk=venda.pk)
    else:
        formset = ItemVendaFormSet(instance=Venda())
    return render(request, 'vendas/registrar_venda.html', {'formset': formset})


@login_required
def vendas_list(request):
    vendas = Venda.objects.all()
    return render(request, 'vendas/vendas_list.html', {'vendas': vendas})


@login_required
def venda_detail(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'vendas/venda_detail.html', {'venda': venda})


@login_required
def venda_delete(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        venda.delete()
        return redirect('vendas_list')
    return render(request, 'vendas/venda_confirm_delete.html', {'venda': venda})


@login_required
def faturamento(request):
    empresa = Empresa.objects.select_related('dono').first()

    if empresa is None:
        raise PermissionDenied('Empresa não configurada.')

    if request.user != empresa.dono:
        raise PermissionDenied('Acesso restrito ao dono da empresa.')

    vendas = Venda.objects.all()
    total_faturamento = sum(venda.total for venda in vendas)
    return render(request, 'vendas/faturamento.html', {'total_faturamento': total_faturamento, 'empresa': empresa})