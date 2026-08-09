from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem', 'categoria']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
