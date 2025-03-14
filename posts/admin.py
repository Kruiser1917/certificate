from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created', 'date_updated']
    list_filter = ['date_created', 'author']
    search_fields = ['title', 'text']
    inlines = [CommentInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'post', 'date_created']
    list_filter = ['date_created', 'author']
    search_fields = ['text']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post') 