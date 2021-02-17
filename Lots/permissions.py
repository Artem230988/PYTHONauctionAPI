from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsLotOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
