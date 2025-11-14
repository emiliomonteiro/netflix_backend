from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Movie
from .serializers import MovieSerializer


class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
def get_all_movies(request):
    """
    GET: Retrieve all movies with pagination, search, and filtering
    POST: Create a new movie
    """
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        genre = request.query_params.get('genre', '')
        min_rating = request.query_params.get('min_rating', None)
        year = request.query_params.get('year', None)
        featured = request.query_params.get('featured', None)
        
        movies = Movie.objects.all()
        
        if search:
            movies = movies.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        if genre:
            movies = movies.filter(genre__iexact=genre)
        
        if min_rating:
            try:
                movies = movies.filter(rating__gte=float(min_rating))
            except ValueError:
                return Response({
                    'error': 'min_rating must be a valid number'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if year:
            try:
                movies = movies.filter(release_year=int(year))
            except ValueError:
                return Response({
                    'error': 'year must be a valid integer'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if featured is not None:
            featured_bool = featured.lower() in ('true', '1', 'yes')
            movies = movies.filter(is_featured=featured_bool)
        
        paginator = MoviePagination()
        paginated_movies = paginator.paginate_queryset(movies, request)
        serializer = MovieSerializer(paginated_movies, many=True)
        
        return paginator.get_paginated_response({
            'count': paginator.page.paginator.count,
            'results': serializer.data
        })
    
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_movies_by_genre(request, genre):
    """
    GET: Retrieve movies filtered by genre
    """
    movies = Movie.objects.filter(genre__iexact=genre)
    
    if not movies.exists():
        return Response({
            'error': f'No movies found for genre: {genre}'
        }, status=status.HTTP_404_NOT_FOUND)
    
    paginator = MoviePagination()
    paginated_movies = paginator.paginate_queryset(movies, request)
    serializer = MovieSerializer(paginated_movies, many=True)
    
    return paginator.get_paginated_response({
        'genre': genre,
        'count': paginator.page.paginator.count,
        'results': serializer.data
    })


@api_view(['GET'])
def get_featured_movies(request):
    """
    GET: Retrieve all featured movies
    """
    featured_movies = Movie.objects.filter(is_featured=True)
    
    paginator = MoviePagination()
    paginated_movies = paginator.paginate_queryset(featured_movies, request)
    serializer = MovieSerializer(paginated_movies, many=True)
    
    return paginator.get_paginated_response({
        'count': paginator.page.paginator.count,
        'results': serializer.data
    })


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def movie_detail(request, pk):
    """
    GET: Retrieve a specific movie by ID
    PUT: Update a movie (full update)
    PATCH: Update a movie (partial update)
    DELETE: Delete a movie
    """
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)