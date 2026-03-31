from rest_framework import viewsets
from .models import Duvida
from rest_framework.response import Response  # <--- ADICIONE ESTA LINHA AQUI!
from .serializers import DuvidaSerializer
from django.utils import timezone

class DuvidaViewSet(viewsets.ModelViewSet):
    queryset = Duvida.objects.all()
    serializer_class = DuvidaSerializer

    def perform_create(self, serializer):
        # O Django pega o usuário do Token JWT e salva no campo usuario_idoso
        serializer.save(usuario_idoso=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # Se for IDOSO, ele só vê as próprias dúvidas
        if user.role == 'IDOSO':
            return Duvida.objects.filter(usuario_idoso=user)
        # Se for PROFISSIONAL, vê todas para responder
        return Duvida.objects.all()
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Só permite responder se o usuário for PROFISSIONAL_SUS
        if request.user.role != 'PROFISSIONAL_SUS':
            return Response({"erro": "Apenas profissionais podem responder."}, status=403)

        # Atualiza os dados da resposta
        instance.texto_resposta = request.data.get('texto_resposta')
        instance.respondido_por = request.user  # Identifica o profissional
        instance.data_resposta = timezone.now() # Registra o horário
        instance.status = 'RESPONDIDA'          # Tira do pendente
        
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)