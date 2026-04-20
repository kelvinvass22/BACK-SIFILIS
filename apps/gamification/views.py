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
    
    def list(self, request, *args, **kwargs):
        try:
            # ADICIONAMOS: usuario__role e usuario__first_name
            ranking = Pontuacao.objects.values(
                'usuario__username',
                'usuario__first_name',
                'usuario__role' 
            ).annotate(
                total_pontos=Sum('pontos')
            ).order_by('-total_pontos')

            # Mapeamos para que o JSON de saída tenha as chaves que o React espera
            data = [
                {
                    "usuario__username": item['usuario__username'],
                    "usuario_nome": item['usuario__first_name'] or item['usuario__username'],
                    "role": item['usuario__role'], # Crucial para o seu Front-end!
                    "total_pontos": item['total_pontos']
                } for item in ranking
            ]
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"ERRO NO RANKING: {e}") 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)