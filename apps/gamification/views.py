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
        # Sobrescrevemos o list para retornar o ranking somado por padrão
        ranking = Pontuacao.objects.values(
            'usuario__username', 
            'usuario__perfil' # Inclua o perfil se quiser mostrar o ícone de idoso/prof
        ).annotate(
            total_pontos=Sum('pontos')
        ).order_by('-total_pontos')
        
        return Response(ranking)

    def perform_create(self, serializer):
        # Garante que o ponto seja salvo no usuário logado
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def ranking_global(self, request):
        # Sua lógica de Top 3 e posição individual
        ranking = Pontuacao.objects.values('usuario__username')\
            .annotate(total_pontos=Sum('pontos'))\
            .order_by('-total_pontos')

        top_3 = ranking[:3]
        
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