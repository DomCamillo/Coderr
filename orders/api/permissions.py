from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    """Only Customer can access"""
    message = 'Only Customer can Create Orders'

    def has_permission(self, request ,view):
            return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'customer'
        )

    class IsBusinessUser(permissions.BasePermission):
        """Only Business User can access"""
        message = 'Only Business-User can change the status'

        def has_permission(self, request, view):
            return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'business'
        )

class IsOrderBusinessUser(permissions.BasePermission):
    message = 'You are not the Business-User of this Order'

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user

