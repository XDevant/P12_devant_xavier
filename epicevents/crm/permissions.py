from rest_framework.permissions import BasePermission


class IsSalesOrAdmin(BasePermission):
    def has_permission(self, request, view):
        groups = ['admin', 'sales']
        return request.user.groups.filter(name__in=groups).exists()


class IsInTeam(BasePermission):
    def has_permission(self, request, view):
        groups = ['admin', 'sales', 'support']
        return request.user.groups.filter(name__in=groups).exists()
