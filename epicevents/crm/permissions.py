from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Client, Contract, Event


class IsSaleContactCRUOrSupportContactReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.groups.filter(name__in=['admin', 'sales', 'support']).exists()
        if request.method in ['POST', 'PUT']:
            return request.user.groups.filter(name__in=['admin', 'sales']).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.groups.filter(name__in=['admin', 'sales', 'support']).exists()
        if request.method in ['POST', 'PUT']:
            return obj.sales_contact == request.user or request.user.groups.filter(name='admin').exists()
        return False


class IsSaleContactCRU(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'PUT']:
            return request.user.groups.filter(name__in=['admin', 'sales']).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.groups.filter(name__in=['admin', 'sales']).exists()
        if request.method in ['POST', 'PUT']:
            return obj.sales_contact == request.user or request.user.groups.filter(name='admin').exists()
        return False


class IsInChargeOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.groups.filter(name__in=['admin', 'sales', 'support']).exists()
        if request.method == 'POST':
            return request.user.groups.filter(name__in=['admin', 'sales']).exists()
        if request.method == 'PUT':
            return request.user.groups.filter(name__in=['admin', 'support']).exists()

