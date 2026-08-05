from django import forms
from django.forms import inlineformset_factory
from .models import Venda, ItemVenda


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = []


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        quantidade = cleaned_data.get('quantidade')

        if not produto or quantidade is None:
            return cleaned_data

        if quantidade <= 0:
            raise forms.ValidationError({'quantidade': 'A quantidade deve ser maior que zero.'})

        if produto.estoque < quantidade:
            raise forms.ValidationError({
                'quantidade': f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}.'
            })

        return cleaned_data


ItemVendaFormSet = inlineformset_factory(
    Venda,
    ItemVenda,
    form=ItemVendaForm,
    extra=2,
    can_delete=False,
)