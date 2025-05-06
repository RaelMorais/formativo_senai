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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

# CRUD para usuario 
class CreateUserView(APIView):
    permission_classes = [IsDiretorOrAdministrador]  # Adiciona a permissão personalizada
    def post(self, request):
        if not request.user.has_perm('app.add_usuario'):  
            return Response({"detail": "Você não tem permissão para criar usuários."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            
            # refresh = RefreshToken.for_user(user)
            # access_token = str(refresh.access_token)
            # refresh_token = str(refresh)

            return Response({
                # 'refresh': refresh_token,
                # 'access': access_token,
                'message':"usuario criado"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateDeleteDetailUsuario(RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsDiretorOrAdministrador]

    def get(self, request, *args, **kwargs):
        try: 
            usuario = self.get_object()
            serializer = self.get_serializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Usuario não encontrando")
            # return Response({'message': 'usuario não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, *args, **kwargs):
        try:
            usuario = self.get_object()
            serializer = self.get_serializer(usuario, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Usuario atualizado com sucesso', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'Erro ao processar'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise Http404("Usuario não encontrando")
        
    def delete(self, request, *args, **kwargs):
        try:
            usuario = self.get_object()
            serializer = self.get_serializer(usuario)
            return Response({'message': 'usuario apagado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Usuario não encontrando")

    
# Para o token 
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# CRUD Disciplinas 
class UpdateDeleteDetailDisciplina(RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    def get(self, request, *args, **kwargs):
        try: 
            disciplina = self.get_object()
            serializer = self.get_serializer(disciplina)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Disciplina não encontrada")
        
    def put(self, request, *args, **kwargs):
        try:
            disciplina = self.get_object()
            serializer = self.get_serializer(disciplina, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Disciplina atualizada com sucesso', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'Erro ao processar'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise Http404("Disciplina não encontrada")
        
    def delete(self, request, *args, **kwargs):
        try:
            disciplina = self.get_object()
            serializer = self.get_serializer(disciplina)
            return Response({'message': 'Disciplina apagado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Disciplina não encontrada")
        

class CreateDisciplina(ListCreateAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Disciplina criada com sucesso','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Erro ao criar Disciplina'}, status=status.HTTP_400_BAD_REQUEST)
    # def create(self, request, *args, **kwargs):
        

#CRUD Salas 
class CreateSala(ListCreateAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sala criada com sucesso','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Erro ao criar Sala'}, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateDeleteDetailSala(RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    def get(self, request, *args, **kwargs):
        try: 
            sala = self.get_object()
            serializer = self.get_serializer(sala)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Sala não encontrada")
        
    def put(self, request, *args, **kwargs):
        try:
            sala = self.get_object()
            serializer = self.get_serializer(sala, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Sala atualizada com sucesso', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'Erro ao processar'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise Http404("Sala não encontrada")
        
    def delete(self, request, *args, **kwargs):
        try:
            sala = self.get_object()
            serializer = self.get_serializer(sala)
            return Response({'message': 'Sala apagada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Sala não encontrada")
        

#CRUD Reservas 
class CreateReservaAmbiente(ListCreateAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaSerializer

    def get(self, request, *args, **kwargs):
        try: 
            reservaAmbiente = self.get_object()
            serializer = self.get_serializer(reservaAmbiente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Ambiente não encontrado")
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ambiente criado com sucesso','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Erro ao criar reserva'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsDiretorOrAdministrador()]

    def get_queryset(self):
        queryset = super().get_queryset()
        professor_id = self.request.query_params.get('professor', None)
        if professor_id:
            queryset = queryset.filter(disc__professor_id=professor_id)
        return queryset

class UpdateDeleteDetailAmbiente(RetrieveUpdateDestroyAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    def get(self, request, *args, **kwargs):
        try: 
            reservaAmbiente = self.get_object()
            serializer = self.get_serializer(reservaAmbiente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Ambiente não encontrado")
        
    def put(self, request, *args, **kwargs):
        try:
            sala = self.get_object()
            serializer = self.get_serializer(sala, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Ambiente atualizado com sucesso'}, serializer.data, status=status.HTTP_200_OK)
            return Response({'message': 'Erro ao processar'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise Http404("Ambiente não encontrado")
        
    def delete(self, request, *args, **kwargs):
        try:
            reservaAmbiente = self.get_object()
            serializer = self.get_serializer(reservaAmbiente)
            return Response({'message': 'Ambiente apagado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Ambiente não encontrado")

#Listagem 
# Professores veem suas proprias disciplinas 
class DisciplinasPorProfessor(ListAPIView):
    serializer_class = DisciplinaSerializer
    permission_classes = [IsProfessor]

    def get_queryset(self):
        return Disciplina.objects.filter(professor=self.request.user)

# Professores veem apenas suas reservas
class ReservasPorProfessor(ListAPIView):
    serializer_class = ReservaSerializer
    permission_classes = [IsProfessor]

    def get_queryset(self):
        return ReservaAmbiente.objects.filter(prof_resp=self.request.user)

    # def get_queryset(self):
    #     return ReservaAmbiente.objects.filter(prof_resp=self.request.user)

# Todos os usuarios
class ListUsuario(ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsDiretorProfessor]

class ListSala(ListAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsDiretorProfessor]




