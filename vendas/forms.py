from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Venda, ItemVenda


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['cliente'].queryset = self.fields['cliente'].queryset.filter(usuario=user)


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['produto'].queryset = self.fields['produto'].queryset.filter(usuario=user)

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

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco']
        