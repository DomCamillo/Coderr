
from rest_framework import permissions


class IsOfferOwner(permissions.BasePermission):
    message = "You only can change own Offers"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# class IsBusinessUser(permissions.BasePermission):
#     """Only business users can create offers"""
#     def has_permission(self, request, view):
#         return hasattr(request.user, 'type') and request.user.type == 'business'