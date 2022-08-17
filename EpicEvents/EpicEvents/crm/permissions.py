from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Client, Contract, Event


class IsSaleContactOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.sales_contact == request.user


class IsInChargeOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        pass
