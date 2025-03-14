from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from blog_project.permissions import IsOwnerOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            # Регистрация доступна всем
            return [permissions.AllowAny()]
        elif self.action in ['retrieve', 'list']:
            # Просмотр доступен авторизованным
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            # Редактирование доступно владельцу и админу
            return [IsOwnerOrAdmin()]
        else:
            # Удаление доступно только админу
            return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_object(self):
        # Если запрос на обновление/получение текущего юзера
        if self.kwargs.get('pk') == 'me' and self.request.user.is_authenticated:
            return self.request.user
        return super().get_object() 