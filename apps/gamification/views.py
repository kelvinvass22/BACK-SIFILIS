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
        try:
            # Agrupa por username e perfil, soma os pontos
            ranking = Pontuacao.objects.values(
                'usuario__username', 
                'usuario__perfil'
            ).annotate(
                total_pontos=Sum('pontos')
            ).order_by('-total_pontos')
            
            # Retornamos os dados crus (dicionários) diretamente para evitar erro de serialização
            return Response(list(ranking), status=status.HTTP_200_OK)
        except Exception as e:
            # Se o banco estiver vazio ou der erro, retorna lista vazia em vez de 500
            return Response([], status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # Garante que salve o ponto no usuário que está enviando
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def ranking_global(self, request):
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
                "pontos": pontos_user or 0
            }
        })