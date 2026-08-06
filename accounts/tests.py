from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class AccountAPITests(TestCase):
    def test_register_api_cria_usuario(self):
        response = self.client.post(reverse('api_register'), {
            'username': 'novo_usuario',
            'email': 'novo@example.com',
            'password': 'senha_segura_123',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='novo_usuario').exists())
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_api_sem_senha_retorna_erro(self):
        response = self.client.post(reverse('api_register'), {
            'username': 'sem_senha',
            'email': 'sem@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_api_com_credenciais_validas(self):
        User.objects.create_user(username='teste', password='senha_segura_123')
        response = self.client.post(reverse('api_login'), {
            'username': 'teste',
            'password': 'senha_segura_123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_api_com_credenciais_invalidas(self):
        response = self.client.post(reverse('api_login'), {
            'username': 'nao_existe',
            'password': 'senha_errada',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)