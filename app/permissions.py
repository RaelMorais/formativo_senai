from rest_framework.permissions import BasePermission

class IsDiretorOrAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.cargo in ['D', 'ADM'])

class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'P'

class IsDiretorProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo in ['D', 'P']

    def has_object_permission(self, request, view, obj):
        if request.user.cargo == 'D':
            return True
        if request.user.cargo == 'P':
            return obj.prof_resp == request.user
        return False
