from .permissions import * 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import * 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import * 
from rest_framework.generics import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model

User = get_user_model()

# CRUD para usuario 
class CreateUserView(APIView):
    permission_classes = [IsDiretorOrAdministrador] 
    @swagger_auto_schema(
        operation_description="Cria um novo usuário. Apenas Diretores ou Administradores com permissão `add_usuario` podem realizar esta operação.",
        request_body=UsuarioSerializer,
        responses={
            201: openapi.Response(description="Usuário criado com sucesso"),
            400: "Dados inválidos",
            403: "Sem permissão"
        }
    )
    def post(self, request):
        if not request.user.has_perm('app.add_usuario'):  
            return Response({"detail": "Você não tem permissão para criar usuários."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            return Response({
                'message':"usuario criado"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Lista todos Usuarios",
        responses={
            200: UsuarioSerializer,
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    
    def get(self, request, *args, **kwargs):
        usuarios = User.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateDeleteDetailUsuario(RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsDiretorOrAdministrador]

# SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- START
    # Swagger Get Method Docs ----------------------------
    @swagger_auto_schema(
        operation_description='Retorna todos os usuarios',
        responses={
            200: UsuarioSerializer,  # Retorna os dados do piloto
            404: 'Não encontrado',  # Caso o piloto não seja encontrado
            400: 'Erro na requisição',  # Erro genérico
        }
    )
    def get(self, request, *args, **kwargs):
        try: 
            usuario = self.get_object()
            serializer = self.get_serializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Usuario não encontrando")
 
    # Swagger Put Method Docs ----------------------------
    @swagger_auto_schema(
            operation_description='Atualiza os usuarios', 
            request_body = UsuarioSerializer, 
            responses={
                201: UsuarioSerializer, 
                404: 'Não Encontrado', 
                500: 'Erro na requisição'
            }
    )
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
    

    # Swagger Delete Method Docs ----------------------------
    @swagger_auto_schema(
        operation_description='Deleta o Usuario',
        responses={
            204: 'Deletado com sucesso!',  
            404: 'Não encontrado',  
            500:  'Erro na requisição'
        }
    )

    def delete(self, request, *args, **kwargs):
        try:
            usuario = self.get_object()
            usuario.delete()
            return Response({'message': 'usuario apagado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Usuario não encontrando")
    
# SWAGGER CONFIGURATIONS -------------------------------------------------------------------------  END 
   
#_______________________________Para o token_________________________________________
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
#_______________________________Para o token_________________________________________


# CRUD Disciplinas 
class CreateDisciplina(ListCreateAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    @swagger_auto_schema(
        operation_description="Cria uma nova Disciplina.",
        request_body=SalaSerializer,
        responses={
            201: openapi.Response("Disciplina criada com sucesso", DisciplinaSerializer),
            400: "Erro ao criar Disciplina"
        }
    )
    # Funções para validação e retornar codigos http 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Disciplina criada com sucesso','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Erro ao criar Disciplina'}, status=status.HTTP_400_BAD_REQUEST)
    # def create(self, request, *args, **kwargs):
        
    @swagger_auto_schema(
        operation_description="Lista todas as disciplinas.",
        responses={
            200: SalaSerializer,
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    
    def get(self, request, *args, **kwargs):
        disciplina = Disciplina.objects.all()
        serializer = DisciplinaSerializer(disciplina, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateDeleteDetailDisciplina(RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsDiretorOrAdministrador]

# SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- START

    # Swagger Get Method Docs ----------------------------
    @swagger_auto_schema(
        operation_description='Retorna todos os usuarios',
        responses={
            200: UsuarioSerializer,  # Retorna os dados do piloto
            404: 'Não encontrado',  # Caso o piloto não seja encontrado
            400: 'Erro na requisição',  # Erro genérico
        }
    )
    def get(self, request, *args, **kwargs):
        try: 
            disciplina = self.get_object()
            serializer = self.get_serializer(disciplina)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Disciplina não encontrada")
        
    # Swagger Put Method Docs ----------------------------
    @swagger_auto_schema(
            operation_description='Atualiza a Disciplina', 
            request_body = DisciplinaSerializer, 
            responses={
                201: DisciplinaSerializer,  
                404: 'Não Encontrado', 
                500: 'Erro na requisição'
            }
    )
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
        
    # Swagger Delete Method Docs ---------------------------- 
    @swagger_auto_schema(
        operation_description='Deleta a disciplina',
        responses={
            204: 'Deletado com sucesso!',  
            404: 'Não encontrado',  
            500:  'Erro na requisição'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            disciplina = self.get_object()
            disciplina.delete()
            return Response({'message': 'Disciplina apagado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Disciplina não encontrada")
    
# SWAGGER CONFIGURATIONS -------------------------------------------------------------------------  END 

    







#CRUD Salas 
class CreateSala(ListCreateAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    @swagger_auto_schema(
        operation_description="Cria uma nova sala.",
        request_body=SalaSerializer,
        responses={
            201: openapi.Response("Sala criada com sucesso", SalaSerializer),
            400: "Erro ao criar Sala"
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sala criada com sucesso','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Erro ao criar Sala'}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Lista todas as salas.",
        responses={
            200: SalaSerializer,
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    
    def get(self, request, *args, **kwargs):
            return super().get(request, *args, **kwargs)
class UpdateDeleteDetailSala(RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsDiretorOrAdministrador]

    # SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- START

    # Swagger Get Method Docs ----------------------------
    @swagger_auto_schema(
            operation_description="Retorna todos os detalhes da sala por ID", 
            responses={
                201: SalaSerializer,  
                404: 'Não Encontrado', 
                500: 'Erro na requisição'
            }

    )
    def get(self, request, *args, **kwargs):
        try: 
            sala = self.get_object()
            serializer = self.get_serializer(sala)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Sala não encontrada")
        
    # Swagger Put Method Docs ----------------------------
    @swagger_auto_schema(
            operation_description='Atualiza a sala por ID.', 
            request_body = SalaSerializer, 
            responses={
                201: SalaSerializer,  
                404: 'Não Encontrado', 
                500: 'Erro na requisição'
            }
    )
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
        
    # Swagger Delete Method Docs ----------------------------
    @swagger_auto_schema(
        operation_description='Deleta a sala por ID',
        responses={
            204: 'Deletado com sucesso!',  
            404: 'Não encontrado',  
            500:  'Erro na requisição'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            sala = self.get_object()
            serializer = self.get_serializer(sala)
            return Response({'message': 'Sala apagada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Sala não encontrada")
    # SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- END 
    # Funções para validação e retornar codigos http 







# Regra: Somente professores ou diretores podem criar reservas de sala 
#CRUD Reservas 
class CreateReservaAmbiente(ListCreateAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaSerializer

    # SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- START
    @swagger_auto_schema(
        operation_description="Lista reservas de ambientes. Pode filtrar por `professor` via query param.",
        manual_parameters=[
            openapi.Parameter(
                'professor',
                openapi.IN_QUERY,
                description="ID do professor para filtrar as reservas",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: ReservaSerializer(many=True),
            401: 'Não autorizado', 
            404: 'Não encontrado', 
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_description="Cria uma nova reserva de ambiente. Apenas Diretores ou Professores autenticados podem criar.",
        request_body=ReservaSerializer,
        responses={
            201: openapi.Response('Criado com sucesso', ReservaSerializer),
            400: 'Erro de validação',
            401: 'Não autorizado',
            403: 'Proibido'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data 
            self.validar_reserva(data)
            serializer.save()
            return Response({'message': 'Ambiente criado com sucesso','data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Erro ao criar reserva'}, status=status.HTTP_400_BAD_REQUEST)
    
    # SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- END 


    # função para validação do método HTTP
    def get(self, request, *args, **kwargs):
        try: 
            reservaAmbiente = self.get_object()
            serializer = self.get_serializer(reservaAmbiente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Ambiente não encontrado")

    # func para validar a reserva 
    def validar_reserva(self, data):
            prof_resp = data['prof_resp']
            sala_reservada = data['sala_reservada']
            data_ini = data['data_ini']
            data_fim = data['data_fim']
            periodo = data['periodo']

            # se a data de inicio for maior que a data de fim, ex: data_ini: 23/05, data_fim: 20/05 
            if data_ini > data_fim:
                raise ValidationError("A data de início não pode ser posterior à data de término.")

            # verificação para disponibilidade do professor, não permitindo estar cadastrado em duas salas na mesma data e período, e retornando mensagem de erro 
            prof_not_available =  ReservaAmbiente.objects.filter(
                prof_resp= prof_resp,
                data_fim__gt = data_ini,
                data_ini__lt = data_fim, 
                periodo= periodo 
            )

            if prof_not_available.exists():
                raise ValidationError ('Professor está indisponivel nesta data')
            
            # verificação se a sala está disponivel 
            sala_not_available = ReservaAmbiente.objects.filter(
                    data_fim__gt = data_ini,
                    data_ini__lt = data_ini, 
                    periodo= periodo, 
                    sala_reservada = sala_reservada
                )
            if sala_not_available.exists():
                raise ValidationError ('Sala já alocada nesta data.')
    # para definir para somente o get não precisar autenticar 
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsDiretorProfessor()] # --> put, delete precisa ser diretor ou professor 

    # retorna as reservas do professor logado com as credencias 
    def get_queryset(self):
        queryset = super().get_queryset()
        professor_id = self.request.query_params.get('professor', None)
        if professor_id:
            queryset = queryset.filter(disc__professor_id=professor_id)
        return queryset

class UpdateDeleteDetailAmbiente(RetrieveUpdateDestroyAPIView):
    
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsDiretorProfessor]

    # SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- START
   
    # Swagger Get Method Docs ----------------------------
    @swagger_auto_schema(
            operation_description="Retorna todos os detalhes da reserva de ambiente por ID", 
            responses={
                201: ReservaSerializer,  
                404: 'Não Encontrado', 
                500: 'Erro na requisição'
            }

    )
    def get(self, request, *args, **kwargs):
        try: 
            reservaAmbiente = self.get_object()
            serializer = self.get_serializer(reservaAmbiente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            raise Http404("Ambiente não encontrado")
    # Swagger Put Method Docs ----------------------------
    @swagger_auto_schema(
            operation_description='Atualiza a reserva de ambiente por ID.', 
            request_body = ReservaSerializer, 
            responses={
                201: ReservaSerializer,  
                404: 'Não Encontrado', 
                500: 'Erro na requisição'
            }
    )
    def put(self, request, *args, **kwargs):
        try:
            sala = self.get_object()
            serializer = self.get_serializer(sala, data=request.data, partial=True)
            if serializer.is_valid():
                data = serializer.validated_data 
                self.validar_reserva(data, instance_id = reserva.pk)
    
                serializer.save()
                return Response({'message': 'Ambiente atualizado com sucesso'}, serializer.data, status=status.HTTP_200_OK)
            return Response({'message': 'Erro ao processar'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise Http404("Ambiente não encontrado")
        
    
     # Swagger Delete Method Docs ----------------------------
    @swagger_auto_schema(
        operation_description='Deleta o ambiente por ID',
        responses={
            204: 'Deletado com sucesso!',  
            404: 'Não encontrado',  
            500:  'Erro na requisição'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            reservaAmbiente = self.get_object()
            serializer = self.get_serializer(reservaAmbiente)
            return Response({'message': 'Ambiente apagado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            raise Http404("Ambiente não encontrado")
    # SWAGGER CONFIGURATIONS ------------------------------------------------------------------------- START

    # validando a criação de ambientes para o método PUT 
    def validar_reserva(self, data, instance_id=None):
            prof_resp = data['prof_resp']
            sala_reservada = data['sala_reservada']
            data_ini = data['data_ini']
            data_fim = data['data_fim']
            periodo = data['periodo']

            if data_ini > data_fim: # --> Não permite que a data de inicio seja posterior a de fim 
                raise ValidationError("A data de início não pode ser posterior à data de término.")

            # --> verificando se o professor está disponivel, caso não irá retornar uma mensagem de erro 
            prof_not_available =  ReservaAmbiente.objects.filter(
                prof_resp= prof_resp,
                data_fim__gt = data_ini,
                data_ini__lt = data_fim, 
                periodo= periodo 
            )

            if prof_not_available.exists():
                raise ValidationError ('Professor está indisponivel nesta data')

            # --> verificando se a sala está disponivel 
            sala_not_available = ReservaAmbiente.objects.filter(
                    data_fim__gt = data_ini,
                    data_ini__lt = data_ini, 
                    periodo= periodo, 
                    sala_reservada = sala_reservada
                )
            if sala_not_available.exists():
                raise ValidationError ('Sala já alocada nesta data.')
            
            # buscando pelo ID para excluir
            if instance_id:
                sala_not_available = sala_not_available.exclude(pk=self.pk)
                prof_not_available = prof_not_available.exclude(pk=self.pk)






#Listagem 
# Professores veem suas proprias disciplinas 
class DisciplinasPorProfessor(ListAPIView):
    serializer_class = DisciplinaSerializer
    permission_classes = [IsProfessor]

    @swagger_auto_schema(
        operation_description="Lista todas as disciplinas atribuídas ao professor autenticado.",
        responses={
            200: DisciplinaSerializer(many=True), 
            404: 'Não encontrado', 
            500: 'Erro interno'
            }
    )
    def get(self, request, *args, **kwargs):
        """---> Retorna disciplinas do professor autenticado <---"""
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return Disciplina.objects.filter(professor=self.request.user)

# Professores veem apenas suas reservas
class ReservasPorProfessor(ListAPIView):
    serializer_class = ReservaSerializer
    permission_classes = [IsProfessor]

    @swagger_auto_schema(
        operation_description="Lista todas as reservas feitas pelo professor autenticado.",
        responses={
            200: ReservaSerializer(many=True),
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    def get(self, request, *args, **kwargs):
        """---> Retorna reservas do professor autenticado <---"""
        return super().get(request, *args, **kwargs)
    

    def get_queryset(self):
        return ReservaAmbiente.objects.filter(prof_resp=self.request.user)

    # def get_queryset(self):
    #     return ReservaAmbiente.objects.filter(prof_resp=self.request.user)

# Todos os usuarios
class ListUsuario(ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsDiretorProfessor]

    @swagger_auto_schema(
        operation_description="Lista todos os usuarios no sistema.",
        responses={
            200: UsuarioSerializer(many=True),
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class ListSala(ListAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsDiretorProfessor]

    @swagger_auto_schema(
        operation_description="Lista todas as salas no sistema.",
        responses={
            200: SalaSerializer(many=True),
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListAmbiente(ListAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsDiretorProfessor]

    @swagger_auto_schema(
        operation_description="Lista todos os ambientes no sistema.",
        responses={
            200: SalaSerializer(many=True),
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListDisciplina(ListAPIView): 
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsDiretorProfessor]

    @swagger_auto_schema(
        operation_description="Lista todos os ambientes no sistema.",
        responses={
            200: DisciplinaSerializer,
            404: 'Não Encontrado', 
            500: 'Erro na requisição', 
            }
    )
    
    def get(self, request, *args, **kwargs):
            return super().get(request, *args, **kwargs)


