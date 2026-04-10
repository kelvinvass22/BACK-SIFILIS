from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

# 1. REGISTRO (Público)
@api_view(['POST'])
@authentication_classes([]) 
@permission_classes([AllowAny]) 
def registrar_usuario(request):
    data = request.data
    try:
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"error": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            first_name=data.get('nome', ''), # Salva o nome completo aqui
            role=data.get('role', 'IDOSO'),
            data_nascimento=data.get('data_nascimento'),
            telefone=data.get('telefone') # TELEFONE ADICIONADO NO REGISTRO
        )
        return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 2. PERFIL (Privado - PATCH)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def gerenciar_perfil(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)