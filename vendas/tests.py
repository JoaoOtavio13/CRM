from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from produtos.models import Produto
from .models import Venda


class VendaEstoqueTests(TestCase):
    def test_nao_permite_venda_quando_estoque_eh_insuficiente(self):
        User = get_user_model()
        user = User.objects.create_user(username='teste', password='123456')
        produto = Produto.objects.create(nome='Notebook', descricao='Teste', preco='1200.00', estoque=1)

        self.client.force_login(user)
        response = self.client.post(reverse('registrar_venda'), {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-produto': produto.pk,
            'form-0-quantidade': '2',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Venda.objects.count(), 0)
        produto.refresh_from_db()
        self.assertEqual(produto.estoque, 1)
        self.assertFalse(response.context['formset'].is_valid())
