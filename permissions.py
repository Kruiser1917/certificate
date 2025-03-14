from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Админу разрешено всё
        if request.user.is_staff:
            return True
        
        # Проверяем, является ли пользователь владельцем объекта
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return obj == request.user  # Для модели User

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return obj == request.user 