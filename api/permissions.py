from rest_framework import permissions


class IsSuperUserBrowseableAPI(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.__class__.__name__ == 'SchemaView':
                return request.user.is_superuser
            else:
                return True
        return False
