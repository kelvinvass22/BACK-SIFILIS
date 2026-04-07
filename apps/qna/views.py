from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Duvida
from .serializers import DuvidaSerializer

class DuvidaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] # <--- Garante que só quem tem token entra
    serializer_class = DuvidaSerializer

    def get_queryset(self):
        user = self.request.user
        
        # 1. ADMIN e PROFISSIONAL: Enxergam absolutamente tudo
        if user.is_staff or user.role in ['ADMIN', 'PROFISSIONAL_SUS']:
            return Duvida.objects.all().order_by('-data_pergunta')
            
        # 2. IDOSO: Só enxerga as dúvidas que ele mesmo criou
        return Duvida.objects.filter(usuario_idoso=user).order_by('-data_pergunta')

    def perform_create(self, serializer):
        # Ao criar, o Django associa automaticamente ao usuário logado (Idoso)
        serializer.save(usuario_idoso=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        # Bloqueia se o usuário for apenas um IDOSO tentando responder
        if user.role == 'IDOSO' and not user.is_staff:
            return Response(
                {"erro": "Você não tem permissão para responder ou editar esta dúvida."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # LÓGICA DE RESPOSTA (Para Profissional ou Admin)
        texto_res = request.data.get('texto_resposta')
        if texto_res:
            instance.texto_resposta = texto_res
            instance.respondido_por = user
            instance.data_resposta = timezone.now()
            instance.status = 'RESPONDIDA'
        
        # O ADMIN pode editar qualquer outro campo se quiser (ex: status, texto da pergunta)
        if user.role == 'ADMIN' or user.is_staff:
            instance.status = request.data.get('status', instance.status)

        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # APENAS ADMIN pode deletar uma dúvida para não haver perda de dados acidental
        if request.user.role != 'ADMIN' and not request.user.is_staff:
            return Response(
                {"erro": "Apenas administradores podem excluir dúvidas."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)