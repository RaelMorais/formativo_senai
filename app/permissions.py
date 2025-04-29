from rest_framework.permissions import BasePermission

class IsDiretor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'D'

class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'P'

class IsEstudante(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'E'

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'ADM'

class IsDiretorProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'D' or request.user.cargo == 'P'
