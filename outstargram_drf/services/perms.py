from rest_framework import permissions

class IsPostOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user == obj.user:
            return True
        return False

    pass


class IsJustForUser(permissions.BasePermission):
    """user 외엔 어떠한 작업도 불가."""
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False
    pass


class IsJustForLikeUser(permissions.BasePermission):
    """like 한 user 외엔 어떠한 작업도 불가."""
    def has_object_permission(self, request, view, obj):
        if request.user == obj.like_user:
            return False
        return False
    pass