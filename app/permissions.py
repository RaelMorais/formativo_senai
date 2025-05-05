from rest_framework.permissions import BasePermission

class IsDiretorOrAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'D' or request.user.cargo == 'ADM'

class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'P'


class IsDiretorProfessor(BasePermission):
    def has_permission(self, request, view, obj):
        if request.user.cargo == ['D', 'P']:
            return True
        return obj.professor == request.user
 