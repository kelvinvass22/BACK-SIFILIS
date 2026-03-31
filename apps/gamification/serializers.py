from rest_framework import serializers
from .models import Pontuacao

class PontuacaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Pontuacao
        fields = ['id', 'usuario', 'usuario_nome', 'jogo', 'pontos', 'data_conquista']
        read_only_fields = ['usuario'] # O usuário é pego pelo token de login