from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# CERTIFIQUE-SE DE QUE ESTE NOME ESTÁ EXATAMENTE ASSIM
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'role', 'data_nascimento', 'telefone', 'cns', 'foto']
        read_only_fields = ['username', 'role']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['username'] = self.user.username
        data['user_id'] = self.user.id
        data['foto'] = self.user.foto.url if self.user.foto else None
        return data

class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            # Decodifica o UID para buscar o usuário
            uid_decoded = urlsafe_base64_decode(attrs['uid']).decode()
            self.user = User.objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'uid': ['Invalid value']})

        # Injeta o formulário que o dj-rest-auth espera no método save()
        self.set_password_form = SetPasswordForm(
            user=self.user,
            data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        return self.set_password_form.save()