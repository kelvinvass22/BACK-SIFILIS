import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render


# Import necessário para usar o sistema do Allauth/Adapter
from allauth.account.forms import ResetPasswordForm

from .serializers import UserSerializer

User_Model = get_user_model()

@api_view(['POST'])
@authentication_classes([]) 
@permission_classes([AllowAny]) 
def registrar_usuario(request):
    data = request.data
    try:
        if User_Model.objects.filter(username=data.get('username')).exists():
            return Response({"error": "Nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        user = User_Model.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            first_name=data.get('nome', ''),
            role=data.get('role', 'IDOSO'),
            data_nascimento=data.get('data_nascimento') or None,
            telefone=data.get('telefone'),
            cns=data.get('cns')
        )
        return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['POST'])
@permission_classes([AllowAny])
def solicitar_reset_whatsapp(request):
    # Import local para evitar o erro "Model class allauth... doesn't declare an explicit app_label"
    from allauth.account.forms import ResetPasswordForm
    
    contato = request.data.get('contato')
    metodo = request.data.get('metodo') # 'email' ou 'whatsapp'
    
    try:
        if metodo == 'email':
            # Dispara o processo do Allauth que usa seu CustomAccountAdapter
            form = ResetPasswordForm(data={'email': contato.strip()})
            if form.is_valid():
                form.save(request)
                return Response({"message": "E-mail de recuperação enviado com sucesso!"}, status=status.HTTP_200_OK)
            return Response({"error": "E-mail inválido ou não cadastrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Mantém a lógica manual apenas para o WhatsApp
            user = User_Model.objects.get(telefone=contato)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = f"https://back-sifilis.onrender.com/reset-password/{uid}/{token}/"
            return Response({"link": link, "message": "Link de WhatsApp gerado com sucesso!"}, status=status.HTTP_200_OK)

    except User_Model.DoesNotExist:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

def password_reset_confirm_view(request, uid, token):
    """
    Renderiza a página HTML para o idoso digitar a nova senha.
    """
    context = {
        'uid': uid,
        'token': token,
        'title': 'Recuperar Senha'
    }
    return render(request, 'registration/password_reset_confirm.html', context)