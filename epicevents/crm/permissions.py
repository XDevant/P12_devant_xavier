from rest_framework.permissions import BasePermission


class IsSaleContactCRUOrSupportContactReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            groups = ['admin', 'sales', 'support']
            return request.user.groups.filter(name__in=groups).exists()
        if request.method in ['POST', 'PUT']:
            groups = ['admin', 'sales']
            return request.user.groups.filter(name__in=groups).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            groups = ['admin', 'sales', 'support']
            return request.user.groups.filter(name__in=groups).exists()
        if request.method in ['POST', 'PUT']:
            check = request.user.groups.filter(name='admin').exists()
            return check or obj.sales_contact == request.user
        return False


class IsSaleContactCRU(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'PUT']:
            groups = ['admin', 'sales']
            return request.user.groups.filter(name__in=groups).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            groups = ['admin', 'sales']
            return request.user.groups.filter(name__in=groups).exists()
        if request.method in ['POST', 'PUT']:
            check = request.user.groups.filter(name='admin').exists()
            return check or obj.sales_contact == request.user
        return False


class IsInChargeOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            groups = ['admin', 'sales', 'support']
            return request.user.groups.filter(name__in=groups).exists()
        if request.method == 'POST':
            groups = ['admin', 'sales']
            return request.user.groups.filter(name__in=groups).exists()
        if request.method == 'PUT':
            groups = ['admin', 'support']
            return request.user.groups.filter(name__in=groups).exists()
