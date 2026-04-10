from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User

@api_view(['POST'])
@authentication_classes([]) # Remove a exigência de JWT aqui
@permission_classes([AllowAny]) # Libera acesso público
def registrar_usuario(request):
    data = request.data
    try:
        # Verifica se o usuário já existe
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"error": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Cria o usuário usando o modelo customizado do AppSífilis
        # No views.py (registrar_usuario)
        user = User.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            role=data.get('role', 'IDOSO'),
            data_nascimento=data.get('data_nascimento'),
            telefone=data.get('telefone') # Adicione isso aqui também!
        )
        return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)