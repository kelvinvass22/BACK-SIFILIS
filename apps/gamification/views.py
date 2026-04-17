from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Pontuacao
from .serializers import PontuacaoSerializer

class PontuacaoViewSet(viewsets.ModelViewSet):
    queryset = Pontuacao.objects.all()
    serializer_class = PontuacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Removi o try/except genérico para você conseguir ver erros no log se algo quebrar
        ranking = Pontuacao.objects.values(
            'usuario__username', 
            'usuario__perfil' 
        ).annotate(
            total_pontos=Sum('pontos')
        ).order_by('-total_pontos')
        
        # O list(ranking) aqui é necessário porque o ranking é um QuerySet de dicionários
        return Response(list(ranking), status=status.HTTP_200_OK)