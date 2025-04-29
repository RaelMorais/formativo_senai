from django.shortcuts import render
from .permissions import * 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import * 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import * 
from rest_framework.generics import *


# Endpoints onde somente o diretor pode alterar 

class CreateUserView(APIView):
    permission_classes = [IsDiretor]  # Adiciona a permissão personalizada
    def post(self, request):
        if not request.user.has_perm('app.add_usuario'):  # Aqui você pode adicionar mais permissões se necessário
            return Response({"detail": "Você não tem permissão para criar usuários."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
        
            return Response({
                'refresh': refresh_token,
                'access': access_token,
                'message':"usuario criado"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateDestroyUsuario(RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsDiretor]

# Endpoints onde o professor e diretor pode alterar 
class ListUsuario(ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsProfessor]

# Diretor e professor 

# Create your views here.
