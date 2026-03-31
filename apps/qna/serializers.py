from rest_framework import serializers
from .models import Duvida

class DuvidaSerializer(serializers.ModelSerializer):
    nome_idoso = serializers.ReadOnlyField(source='usuario_idoso.username')
    nome_profissional = serializers.ReadOnlyField(source='respondido_por.username')
    class Meta:
        model = Duvida
        fields = [
            'id', 'usuario_idoso', 'nome_idoso', 'texto_pergunta', 'data_pergunta', 
            'status', 'texto_resposta', 'respondido_por', 'nome_profissional', 'data_resposta'
        ]
        # ADICIONE ESTES CAMPOS COMO READ_ONLY
        read_only_fields = ['status', 'usuario_idoso', 'respondido_por', 'data_resposta']