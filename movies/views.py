from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer

@api_view(['GET'])
def get_all_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response({
        'count': movies.count(),
        'movies': serializer.data
    })


@api_view(['GET'])
def get_movies_by_genre(request, genre):
    movies = Movie.objects.filter(genre__iexact=genre)
    
    if not movies.exists():
        return Response({
            'error': f'No movies found for genre: {genre}'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MovieSerializer(movies, many=True)
    return Response({
        'genre': genre,
        'count': movies.count(),
        'movies': serializer.data
    })


@api_view(['GET'])
def get_featured_movies(request):
    featured_movies = Movie.objects.filter(is_featured=True)
    serializer = MovieSerializer(featured_movies, many=True)
    return Response({
        'count': featured_movies.count(),
        'movies': serializer.data
    })