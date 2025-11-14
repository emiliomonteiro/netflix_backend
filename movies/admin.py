from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_year', 'rating', 'is_featured', 'created_at')
    list_filter = ('genre', 'is_featured', 'release_year', 'rating')
    search_fields = ('title', 'description', 'genre')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
