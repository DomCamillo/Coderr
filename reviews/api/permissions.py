from rest_framework import permissions

class ISReviewAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors of a review to edit or delete it.
    """

    def has_object_permission(self, request, view):
            return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'business'
        )

