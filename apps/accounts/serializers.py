from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Adicionei 'foto' e 'cns' aqui
        fields = ['id', 'username', 'email', 'first_name', 'role', 'data_nascimento', 'telefone', 'cns', 'foto']
        read_only_fields = ['username', 'role']
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Injeta os dados necessários para o App
        data['role'] = self.user.role
        data['username'] = self.user.username
        data['user_id'] = self.user.id
        # Se quiser que a foto carregue no login:
        data['foto'] = self.user.foto.url if self.user.foto else None
        return data