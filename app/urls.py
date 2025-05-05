from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Criar itens - > Usuario, Disciplina, Ambiente e Sala
    path("criar/usuario/", CreateUserView.as_view()),
    path('criar/disciplina/', CreateDisciplina.as_view()),
    path('criar/ambiente/', CreateReservaAmbiente.as_view()),
    path("criar/sala/", CreateSala.as_view()),

    # Endpoints para detalhe, update e delete --> Usando o <id>
    path('ambiente/<int:pk>', UpdateDeleteDetailAmbiente.as_view()),
    path('disciplina/<int:pk>', UpdateDeleteDetailDisciplina.as_view()),
    path("usuario/<int:pk>", UpdateDeleteDetailUsuario.as_view()),
    path("sala/<int:pk>", UpdateDeleteDetailSala.as_view()),

    # Endpoints apenas para visualização do diretor e professor 
    path("usuario/", ListUsuario.as_view()),
    path("sala/", ListSala.as_view()),

    # Endpoints apenas para visualização de reservas por professor e disciplina por professor 
    path('reservas/', ReservasPorProfessor.as_view()), 
    path("disciplina/", DisciplinasPorProfessor.as_view()), 

    # Para obter o token --> LoginView retorna valoes personalizados definidos em serializers.py <--
    path('token/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
