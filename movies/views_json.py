import json
import os
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

JSON_FILE_PATH = os.path.join(settings.BASE_DIR, 'movies', 'data', 'movies.json')

def load_movies_from_json():
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('movies', [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


@api_view(['GET'])
def get_all_movies(request):
    movies = load_movies_from_json()
    return Response({
        'count': len(movies),
        'movies': movies
    })


@api_view(['GET'])
def get_movies_by_genre(request, genre):
    movies = load_movies_from_json()
    filtered_movies = [
        movie for movie in movies 
        if movie.get('genre', '').lower() == genre.lower()
    ]
    
    if not filtered_movies:
        return Response({
            'error': f'No movies found for genre: {genre}'
        }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'genre': genre,
        'count': len(filtered_movies),
        'movies': filtered_movies
    })


@api_view(['GET'])
def get_featured_movies(request):
    movies = load_movies_from_json()
    featured_movies = [
        movie for movie in movies 
        if movie.get('is_featured', False)
    ]
    
    return Response({
        'count': len(featured_movies),
        'movies': featured_movies
    })