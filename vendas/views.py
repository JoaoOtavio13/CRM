from decimal import Decimal
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import admin_required
from .models import Cliente, Venda
from .forms import ItemVendaFormSet, ClienteForm, VendaForm


@login_required
def registrar_venda(request):
    form_kwargs = {'user': request.user}
    if request.method == 'POST':
        venda = Venda(usuario=request.user)
        venda_form = VendaForm(request.POST, instance=venda, user=request.user)
        formset = ItemVendaFormSet(request.POST, instance=venda, form_kwargs=form_kwargs)
        if venda_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    venda = venda_form.save()
                    formset.instance = venda
                    formset.save()
                    venda.refresh_from_db()
            except ValidationError as exc:
                messages.error(request, exc.messages[0] if exc.messages else 'Não foi possível registrar a venda.')
                return render(request, 'vendas/registrar_venda.html', {'formset': formset, 'venda_form': venda_form})
            return redirect('venda_detail', pk=venda.pk)
        else:
            messages.error(request, 'Corrija os itens da venda antes de salvar.')
    else:
        venda_form = VendaForm(user=request.user)
        formset = ItemVendaFormSet(instance=Venda(), form_kwargs=form_kwargs)
    return render(request, 'vendas/registrar_venda.html', {'formset': formset, 'venda_form': venda_form})


@login_required
def vendas_list(request):
    vendas = Venda.objects.filter(usuario=request.user)
    return render(request, 'vendas/vendas_list.html', {'vendas': vendas})


@login_required
def venda_detail(request, pk):
    venda = get_object_or_404(Venda, pk=pk, usuario=request.user)
    return render(request, 'vendas/venda_detail.html', {'venda': venda})


@login_required
def venda_delete(request, pk):
    venda = get_object_or_404(Venda, pk=pk, usuario=request.user)
    if request.method == 'POST':
        venda.delete()
        return redirect('vendas_list')
    return render(request, 'vendas/venda_confirm_delete.html', {'venda': venda})


@login_required
@admin_required
def faturamento(request):
    vendas = Venda.objects.filter(usuario=request.user)
    total_faturamento = sum((venda.total for venda in vendas), Decimal('0.00'))
    nome_usuario = request.user.username
    return render(request, 'vendas/faturamento.html', {
        'total_faturamento': total_faturamento,
        'nome_usuario': nome_usuario,
    })

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    return render(request, 'vendas/clientes_list.html', {'clientes': clientes})

@login_required
def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            return redirect('vendas_list')
    else:
        form = ClienteForm()
    return render(request, 'vendas/cadastro_cliente.html', {'form': form})