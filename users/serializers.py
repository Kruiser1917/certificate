from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from .models import validate_email_domain

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'birth_date', 'date_created', 'date_updated']
        read_only_fields = ['date_created', 'date_updated']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_email(self, value):
        validate_email_domain(value)
        return value
    
    def validate_password(self, value):
        from users.models import validate_password as custom_validate_password
        custom_validate_password(value)
        return value
    
    def create(self, validated_data):
        # validate_password уже вызван в процессе валидации
        user = User.objects.create_user(**validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'birth_date'] 