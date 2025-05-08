from rest_framework.permissions import BasePermission

class IsDiretorOrAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'D' or request.user.cargo == 'ADM'

class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'P'


from rest_framework.permissions import BasePermission

class IsDiretorProfessor(BasePermission):
    def has_permission(self, request, view):
        # Permite acesso a usuários autenticados com cargo 'D' (Diretor) ou 'P' (Professor)
        return request.user.is_authenticated and request.user.cargo in ['D', 'P']
    def has_object_permission(self, request, view, obj):
        # Para operações em objetos específicos (GET, PUT, DELETE), verifica se o usuário é Diretor ou Professor
        # Diretores têm acesso total, Professores só podem acessar reservas onde são responsáveis
        if request.user.cargo == 'D':
            return True  # Diretores têm permissão total
        if request.user.cargo == 'P':
            # Professores só podem acessar reservas onde são o prof_resp
            return obj.prof_resp == request.user
        return False