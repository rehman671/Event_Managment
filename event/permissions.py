from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow unauthenticated access for GET method
        if request.method == "GET":
            return True

        # Require authentication for other methods
        return request.user and request.user.is_authenticated


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
