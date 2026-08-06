from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Produto

User = get_user_model()


class ProdutoAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha_segura_123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_listar_produtos_requer_autenticacao(self):
        client = APIClient()
        response = client.get('/api/produtos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_produtos_do_usuario(self):
        Produto.objects.create(usuario=self.user, nome='Notebook', descricao='Teste', preco='1200.00', estoque=5)
        response = self.client.get('/api/produtos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_criar_produto(self):
        response = self.client.post('/api/produtos/', {
            'nome': 'Mouse',
            'descricao': 'Mouse sem fio',
            'preco': '50.00',
            'estoque': 10,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 1)
        self.assertEqual(Produto.objects.first().usuario, self.user)

    def test_criar_produto_com_estoque_negativo(self):
        response = self.client.post('/api/produtos/', {
            'nome': 'Mouse',
            'descricao': 'Mouse sem fio',
            'preco': '50.00',
            'estoque': -1,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detalhe_produto(self):
        produto = Produto.objects.create(usuario=self.user, nome='Notebook', descricao='Teste', preco='1200.00', estoque=5)
        response = self.client.get(f'/api/produtos/{produto.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Notebook')
        self.assertEqual(response.data['estoque'], 5)

    def test_editar_produto(self):
        produto = Produto.objects.create(usuario=self.user, nome='Notebook', descricao='Teste', preco='1200.00', estoque=5)
        response = self.client.put(f'/api/produtos/{produto.pk}/', {
            'nome': 'Notebook Pro',
            'descricao': 'Teste editado',
            'preco': '1500.00',
            'estoque': 3,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        produto.refresh_from_db()
        self.assertEqual(produto.nome, 'Notebook Pro')
        self.assertEqual(produto.estoque, 3)

    def test_deletar_produto(self):
        produto = Produto.objects.create(usuario=self.user, nome='Notebook', descricao='Teste', preco='1200.00', estoque=5)
        response = self.client.delete(f'/api/produtos/{produto.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Produto.objects.count(), 0)

    def test_usuario_nao_ve_produtos_de_outro_usuario(self):
        outro_usuario = User.objects.create_user(username='outro', password='senha_segura_123')
        Produto.objects.create(usuario=outro_usuario, nome='Produto do outro', descricao='Teste', preco='100.00', estoque=5)
        response = self.client.get('/api/produtos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)