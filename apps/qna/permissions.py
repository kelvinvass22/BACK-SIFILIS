from rest_framework import permissions

class IsIdoso(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'IDOSO'

class IsProfissional(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'PROFISSIONAL_SUS'