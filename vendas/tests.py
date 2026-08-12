from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Empresa, Perfil
from produtos.models import Produto
from .models import Venda, ItemVenda

User = get_user_model()


class FaturamentoAPITests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='usuario1', password='senha_segura_123')
        self.empresa = Empresa.objects.create(nome='Empresa do Usuário', cnpj='12345678000100')
        Perfil.objects.create(
            user=self.usuario,
            nome='Dono',
            telefone='11999999999',
            cargo='Admin',
            cpf='12345678901',
            empresa=self.empresa,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.usuario)

    def test_faturamento_requer_autenticacao(self):
        client = APIClient()
        response = client.get('/api/faturamento/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_faturamento_retorna_total_do_usuario_logado(self):
        produto = Produto.objects.create(usuario=self.usuario, nome='Notebook', descricao='Teste', preco='100.00', estoque=10)
        venda = Venda.objects.create(usuario=self.usuario)
        ItemVenda.objects.create(venda=venda, produto=produto, quantidade=2)
        venda.refresh_from_db()

        response = self.client.get('/api/faturamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['usuario'], 'usuario1')
        self.assertEqual(response.data['total_faturamento'], '200.00')
        self.assertEqual(response.data['total_vendas'], 1)

    def test_faturamento_nao_inclui_vendas_de_outros_usuarios(self):
        outro_usuario = User.objects.create_user(username='usuario2', password='senha_segura_123')
        produto = Produto.objects.create(usuario=self.usuario, nome='Notebook', descricao='Teste', preco='100.00', estoque=10)
        venda_outro = Venda.objects.create(usuario=outro_usuario)
        ItemVenda.objects.create(venda=venda_outro, produto=produto, quantidade=2)
        venda_outro.refresh_from_db()

        response = self.client.get('/api/faturamento/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_faturamento'], '0.00')
        self.assertEqual(response.data['total_vendas'], 0)

    def test_faturamento_restringe_acesso_ao_dono_da_empresa(self):
        empresa = Empresa.objects.create(nome='Empresa Teste', cnpj='12345678000199')
        self.usuario_perfil = Perfil.objects.get(user=self.usuario)
        self.usuario_perfil.empresa = empresa
        self.usuario_perfil.save(update_fields=['empresa'])

        outro_usuario = User.objects.create_user(username='usuario2', password='senha_segura_123')
        Perfil.objects.create(user=outro_usuario, nome='Vendedor', telefone='11988888888', cargo='Vendedor', cpf='10987654321', empresa=empresa, is_dono=False)

        produto = Produto.objects.create(usuario=self.usuario, nome='Notebook', descricao='Teste', preco='100.00', estoque=10)
        venda = Venda.objects.create(usuario=self.usuario)
        ItemVenda.objects.create(venda=venda, produto=produto, quantidade=2)
        venda.refresh_from_db()

        client = APIClient()
        client.force_authenticate(user=outro_usuario)

        response = client.get('/api/faturamento/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class VendaListAPITests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='usuario1', password='senha_segura_123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.usuario)

    def test_listar_vendas_requer_autenticacao(self):
        client = APIClient()
        response = client.get('/api/vendas/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_vendas_do_usuario(self):
        produto = Produto.objects.create(usuario=self.usuario, nome='Notebook', descricao='Teste', preco='100.00', estoque=10)
        venda = Venda.objects.create(usuario=self.usuario)
        ItemVenda.objects.create(venda=venda, produto=produto, quantidade=2)
        venda.refresh_from_db()

        response = self.client.get('/api/vendas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['total'], '200.00')

    def test_listar_vendas_nao_inclui_vendas_de_outros(self):
        outro_usuario = User.objects.create_user(username='usuario2', password='senha_segura_123')
        produto = Produto.objects.create(usuario=self.usuario, nome='Notebook', descricao='Teste', preco='100.00', estoque=10)
        venda_outro = Venda.objects.create(usuario=outro_usuario)
        ItemVenda.objects.create(venda=venda_outro, produto=produto, quantidade=2)
        venda_outro.refresh_from_db()

        response = self.client.get('/api/vendas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class VendaNumeroSequencialTests(TestCase):
    def setUp(self):
        self.usuario1 = User.objects.create_user(username='usuario1', password='senha_segura_123')
        self.usuario2 = User.objects.create_user(username='usuario2', password='senha_segura_123')

    def test_numero_venda_sequencial_por_usuario(self):
        venda1_u1 = Venda.objects.create(usuario=self.usuario1)
        venda2_u1 = Venda.objects.create(usuario=self.usuario1)
        venda1_u2 = Venda.objects.create(usuario=self.usuario2)

        self.assertEqual(venda1_u1.numero, 1)
        self.assertEqual(venda2_u1.numero, 2)
        self.assertEqual(venda1_u2.numero, 1)

    def test_numero_venda_continua_apos_exclusao(self):
        venda1_u1 = Venda.objects.create(usuario=self.usuario1)
        venda2_u1 = Venda.objects.create(usuario=self.usuario1)
        venda1_u1.delete()

        venda3_u1 = Venda.objects.create(usuario=self.usuario1)
        self.assertEqual(venda3_u1.numero, 3)

    def test_numero_venda_independente_entre_usuarios(self):
        venda1_u1 = Venda.objects.create(usuario=self.usuario1)
        venda1_u2 = Venda.objects.create(usuario=self.usuario2)
        venda2_u2 = Venda.objects.create(usuario=self.usuario2)
        venda2_u1 = Venda.objects.create(usuario=self.usuario1)

        self.assertEqual(venda1_u1.numero, 1)
        self.assertEqual(venda1_u2.numero, 1)
        self.assertEqual(venda2_u2.numero, 2)
        self.assertEqual(venda2_u1.numero, 2)


class VendaEstoqueTests(TestCase):
    def test_nao_permite_venda_quando_estoque_eh_insuficiente(self):
        User = get_user_model()
        user = User.objects.create_user(username='teste', password='123456')
        produto = Produto.objects.create(usuario=user, nome='Notebook', descricao='Teste', preco='1200.00', estoque=1)

        self.client.force_login(user)
        response = self.client.post('/vendas/nova/', {
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