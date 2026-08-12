from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Perfil

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    nome = serializers.CharField(max_length=100, required=False, allow_blank=True)
    empresa_nome = serializers.CharField(max_length=100, required=True, allow_blank=False, error_messages={
        'blank': 'O campo empresa é obrigatório.',
        'required': 'O campo empresa é obrigatório.',
    })

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'nome', 'empresa_nome')

    def create(self, validated_data):
        nome = validated_data.pop('nome', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        Perfil.objects.create(user=user, nome=nome)
        return user
