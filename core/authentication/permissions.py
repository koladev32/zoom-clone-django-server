from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        basename = view.basename

        if basename in ['room']:
            if request.method not in permissions.SAFE_METHODS:
                return view.action in ['create'] and request.user.is_authenticated
            else:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        if view.basename in ['user']:
            return obj == request.user

        return False
