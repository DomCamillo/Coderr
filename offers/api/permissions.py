
from rest_framework import permissions


class IsOfferOwner(permissions.BasePermission):
    message = "You only can change own Offers"
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


