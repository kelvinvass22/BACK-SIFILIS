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

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def ranking_global(self, request):
        # Soma todos os pontos por usuário e ordena
        ranking = Pontuacao.objects.values('usuario__username')\
            .annotate(total_pontos=Sum('pontos'))\
            .order_by('-total_pontos')

        top_3 = ranking[:3]
        
        # Encontra a posição do usuário logado
        posicao_user = 0
        pontos_user = 0
        for i, item in enumerate(ranking):
            if item['usuario__username'] == request.user.username:
                posicao_user = i + 1
                pontos_user = item['total_pontos']
                break

        return Response({
            "top_3": list(top_3),
            "meu_ranking": {
                "posicao": posicao_user,
                "pontos": pontos_user
            }
        })