from rest_framework import viewsets, permissions
from .models import Pontuacao
from .serializers import PontuacaoSerializer

class PontuacaoViewSet(viewsets.ModelViewSet):
    queryset = Pontuacao.objects.all()
    serializer_class = PontuacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Salva a pontuação vinculada ao idoso que está jogando
        serializer.save(usuario=self.request.user)

    