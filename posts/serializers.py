from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserSerializer
from django.utils import timezone

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'post', 'date_created', 'date_updated']
        read_only_fields = ['author', 'date_created', 'date_updated']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'image', 'author', 'comments', 'date_created', 'date_updated']
        read_only_fields = ['author', 'date_created', 'date_updated']
    
    def validate_title(self, value):
        from posts.models import validate_title
        validate_title(value)
        return value
    
    def validate(self, data):
        user = self.context['request'].user
        from posts.models import validate_age
        validate_age(user)
        return data
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data) 