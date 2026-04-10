from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'data_nascimento', 'telefone'] # ADICIONE 'telefone'


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Chama a validação padrão (que verifica senha e gera o token)
        data = super().validate(attrs)

        # Aqui injetamos os dados do seu modelo User no JSON de resposta
        # O self.user é o usuário que acabou de logar no PostgreSQL
        data['role'] = self.user.role
        data['username'] = self.user.username
        data['user_id'] = self.user.id

        return data