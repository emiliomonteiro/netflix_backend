import json
import os
from datetime import datetime
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

JSON_FILE_PATH = os.path.join(settings.BASE_DIR, 'movies', 'data', 'movies.json')
os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)


def load_movies():
    """Carrega filmes do arquivo JSON"""
    try:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file).get('movies', [])
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_movies(movies):
    """Salva filmes no arquivo JSON"""
    try:
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump({'movies': movies}, file, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def validate_movie(data, is_update=False):
    """Valida os dados do filme"""
    errors = {}
    validator = URLValidator()
    
    if 'rating' in data:
        try:
            rating = float(data['rating'])
            if not 0 <= rating <= 10:
                errors['rating'] = ['Nota deve estar entre 0 e 10']
        except (ValueError, TypeError):
            errors['rating'] = ['Rating deve ser um número válido']
    
    if 'release_year' in data:
        try:
            year = int(data['release_year'])
            if year < 1888:
                errors['release_year'] = ['Ano de lançamento não pode ser antes de 1888']
            elif year > 2100:
                errors['release_year'] = ['Ano de lançamento parece muito distante no futuro']
        except (ValueError, TypeError):
            errors['release_year'] = ['Ano de lançamento deve ser um número inteiro válido']
    
    if 'duration_minutes' in data:
        try:
            duration = int(data['duration_minutes'])
            if duration <= 0:
                errors['duration_minutes'] = ['Duração deve ser maior que 0']
            elif duration > 600:
                errors['duration_minutes'] = ['Duração parece muito longa']
        except (ValueError, TypeError):
            errors['duration_minutes'] = ['Duração deve ser um número inteiro válido']
    
    for url_field in ['thumbnail_url', 'video_url']:
        if url_field in data:
            try:
                validator(data[url_field])
            except ValidationError:
                errors[url_field] = [f'Formato de URL inválido para {url_field.replace("_url", "")}']
    
    if not is_update:
        required = ['title', 'description', 'genre', 'release_year', 'duration_minutes', 'rating', 'thumbnail_url', 'video_url']
        for field in required:
            if field not in data or not data[field]:
                errors[field] = ['Este campo é obrigatório.']
    
    return errors


def paginate_response(movies, request):
    """Aplica paginação e retorna resposta"""
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginator.max_page_size = 100
    page = paginator.paginate_queryset(movies, request)
    
    if page is not None:
        return paginator.get_paginated_response({
            'count': len(movies),
            'results': page
        })
    return Response({'count': len(movies), 'results': movies})


def find_movie(movies, pk):
    """Encontra filme por ID e retorna (movie, index)"""
    for i, m in enumerate(movies):
        if m.get('id') == pk:
            return m, i
    return None, None


@api_view(['GET', 'POST'])
def get_all_movies(request):
    """GET: Lista filmes com filtros | POST: Cria novo filme"""
    if request.method == 'GET':
        movies = load_movies()
        params = request.query_params
        
        if params.get('search'):
            search = params['search'].lower()
            movies = [m for m in movies if search in m.get('title', '').lower() or search in m.get('description', '').lower()]
        
        if params.get('genre'):
            movies = [m for m in movies if m.get('genre', '').lower() == params['genre'].lower()]
        
        if params.get('min_rating'):
            try:
                min_rating = float(params['min_rating'])
                movies = [m for m in movies if float(m.get('rating', 0)) >= min_rating]
            except ValueError:
                return Response({'error': 'min_rating deve ser um número válido'}, status=status.HTTP_400_BAD_REQUEST)
        
        if params.get('year'):
            try:
                year = int(params['year'])
                movies = [m for m in movies if m.get('release_year') == year]
            except ValueError:
                return Response({'error': 'year deve ser um número inteiro válido'}, status=status.HTTP_400_BAD_REQUEST)
        
        if params.get('featured') is not None:
            featured = params['featured'].lower() in ('true', '1', 'yes')
            movies = [m for m in movies if m.get('is_featured', False) == featured]
        
        return paginate_response(movies, request)
    
    # POST
    data = request.data
    errors = validate_movie(data, is_update=False)
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    movies = load_movies()
    new_id = max((m.get('id', 0) for m in movies), default=0) + 1
    now = datetime.now().isoformat()
    
    new_movie = {
        'id': new_id,
        'title': data['title'],
        'description': data['description'],
        'genre': data['genre'],
        'release_year': int(data['release_year']),
        'duration_minutes': int(data['duration_minutes']),
        'rating': float(data['rating']),
        'thumbnail_url': data['thumbnail_url'],
        'video_url': data['video_url'],
        'is_featured': data.get('is_featured', False),
        'created_at': now,
        'updated_at': now
    }
    
    movies.append(new_movie)
    if save_movies(movies):
        return Response(new_movie, status=status.HTTP_201_CREATED)
    return Response({'error': 'Erro ao salvar o filme'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_movies_by_genre(request, genre):
    """GET: Lista filmes por gênero"""
    movies = [m for m in load_movies() if m.get('genre', '').lower() == genre.lower()]
    
    if not movies:
        return Response({'error': f'Nenhum filme encontrado para o gênero: {genre}'}, status=status.HTTP_404_NOT_FOUND)
    
    response = paginate_response(movies, request)
    if hasattr(response, 'data'):
        response.data['genre'] = genre
    return response


@api_view(['GET'])
def get_featured_movies(request):
    """GET: Lista filmes em destaque"""
    movies = [m for m in load_movies() if m.get('is_featured', False)]
    return paginate_response(movies, request)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def movie_detail(request, pk):
    """GET: Busca filme | PUT: Atualiza completo | PATCH: Atualiza parcial | DELETE: Remove"""
    movies = load_movies()
    movie, index = find_movie(movies, pk)
    
    if movie is None:
        return Response({'error': 'Filme não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(movie)
    
    if request.method == 'DELETE':
        movies.pop(index)
        if save_movies(movies):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Erro ao deletar o filme'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # PUT ou PATCH
    data = request.data
    errors = validate_movie(data, is_update=(request.method == 'PATCH'))
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        updated = {
            'id': pk,
            'title': data['title'],
            'description': data['description'],
            'genre': data['genre'],
            'release_year': int(data['release_year']),
            'duration_minutes': int(data['duration_minutes']),
            'rating': float(data['rating']),
            'thumbnail_url': data['thumbnail_url'],
            'video_url': data['video_url'],
            'is_featured': data.get('is_featured', False),
            'created_at': movie.get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }
    else:  # PATCH
        updated = movie.copy()
        for key, value in data.items():
            if key in ['title', 'description', 'genre', 'thumbnail_url', 'video_url']:
                updated[key] = value
            elif key == 'release_year':
                updated[key] = int(value)
            elif key == 'duration_minutes':
                updated[key] = int(value)
            elif key == 'rating':
                updated[key] = float(value)
            elif key == 'is_featured':
                updated[key] = bool(value)
        updated['updated_at'] = datetime.now().isoformat()
    
    movies[index] = updated
    if save_movies(movies):
        return Response(updated)
    return Response({'error': 'Erro ao salvar o filme'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
