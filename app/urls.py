from django.urls import path
from . import views
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Criar itens - > Usuario, Disciplina, Ambiente e Sala -> Só para o diretor e Administrador 
    path("usuario/", CreateUserView.as_view()),
    path('disciplina/', CreateDisciplina.as_view()),
    path('ambiente/', CreateReservaAmbiente.as_view()),
    path("sala/", CreateSala.as_view()),

    # Endpoints para detalhe, update e delete --> Usando o <id>
    path('ambiente/<int:pk>', UpdateDeleteDetailAmbiente.as_view()),
    # Diretor ou administrador tem acesso 
    path('disciplina/<int:pk>', UpdateDeleteDetailDisciplina.as_view()), 
    path("usuario/<int:pk>", UpdateDeleteDetailUsuario.as_view()),
    path("sala/<int:pk>", UpdateDeleteDetailSala.as_view()),

    # Endpoints apenas para visualização do diretor e professor 
    path("usuarios/", ListUsuario.as_view()),
    path("salas/", ListSala.as_view()),
    path('ambientes/', ListAmbiente.as_view()),
    path('disciplinas/', ListDisciplina.as_view()),

    # Endpoints apenas para visualização de reservas por professor e disciplina por professor 
    path('listar/reservas/', ReservasPorProfessor.as_view()), 
    path("listar/disciplina/", DisciplinasPorProfessor.as_view()), 

    # Para obter o token --> LoginView retorna valoes personalizados definidos em serializers.py <--
    path('token/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="eSCOLAR",
        default_version='v1',
        description="Documentação API Formativa - Senai 'Roberto Mange'",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('redoc/', view=schema_view.with_ui('redoc', cache_timeout=0)), # --> Com redoc 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # --> Com Swaager
]
