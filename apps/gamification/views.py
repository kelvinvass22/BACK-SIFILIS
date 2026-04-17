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
            ranking = Pontuacao.objects.values(
                'usuario__username' # Deixe apenas campos que existem no User
            ).annotate(
                total_pontos=Sum('pontos')
            ).order_by('-total_pontos')
            
            return Response(list(ranking), status=status.HTTP_200_OK)
        except Exception as e:
            # Isso vai te ajudar a ver o erro real no log do Render/Terminal
            print(f"ERRO NO RANKING: {e}") 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)