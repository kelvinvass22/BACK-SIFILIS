from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

# views.py

@api_view(['POST'])
@authentication_classes([]) 
@permission_classes([AllowAny]) 
def registrar_usuario(request):
    data = request.data
    try:
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"error": "Nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        # Cuidado com campos nulos na data de nascimento
        data_nasc = data.get('data_nascimento')
        if not data_nasc:
            data_nasc = None

        user = User.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            first_name=data.get('nome', ''),
            role=data.get('role', 'IDOSO'),
            data_nascimento=data_nasc,
            telefone=data.get('telefone'),
            cns=data.get('cns') # <--- FALTAVA ISSO AQUI
        )
        return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Retorna o erro real para o console do celular
        print(f"Erro no registro: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)