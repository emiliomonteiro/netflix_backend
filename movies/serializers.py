from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'genre',
            'release_year',
            'duration_minutes',
            'rating',
            'thumbnail_url',
            'video_url',
            'is_featured',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        """Validate rating is between 0 and 10"""
        if value < 0 or value > 10:
            raise serializers.ValidationError("Rating must be between 0 and 10")
        return value
    
    def validate_release_year(self, value):
        """Validate release year is reasonable"""
        if value < 1888:  
            raise serializers.ValidationError("Release year cannot be before 1888")
        if value > 2100:  
            raise serializers.ValidationError("Release year seems too far in the future")
        return value
    
    def validate_duration_minutes(self, value):
        """Validate duration is positive"""
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than 0")
        if value > 600:  
            raise serializers.ValidationError("Duration seems unreasonably long")
        return value
    
    def validate_thumbnail_url(self, value):
        """Validate URL format"""
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid URL format for thumbnail")
        return value
    
    def validate_video_url(self, value):
        """Validate URL format"""
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid URL format for video")
        return value