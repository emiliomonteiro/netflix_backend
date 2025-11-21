import json
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404

JSON_FILE_PATH = os.path.join(settings.BASE_DIR, 'movies', 'data', 'movies.json')


def load_movies():
    """Carrega filmes do arquivo JSON"""
    try:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file).get('movies', [])
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def find_movie_by_imdb_id(imdb_id):
    """Encontra filme por imdb_id no JSON"""
    movies = load_movies()
    for movie in movies:
        if movie.get('imdb_id') == imdb_id:
            return movie
    return None


@login_required
def home(request):
    """Exibe catálogo de filmes do JSON"""
    movies = load_movies()
    # Filtrar apenas filmes que têm imdb_id (vindos do OMDB)
    movies_with_imdb = [m for m in movies if m.get('imdb_id')]
    return render(request, "catalog/home.html", {"filmes": movies_with_imdb})


def detalhes_filme(request, imdb_id):
    """Exibe detalhes do filme buscando do JSON"""
    movie = find_movie_by_imdb_id(imdb_id)
    
    if not movie:
        raise Http404("Filme não encontrado")
    
    # Converter formato JSON para formato compatível com template (campos OMDB)
    filme_data = {
        'Title': movie.get('title', ''),
        'Year': str(movie.get('release_year', '')),
        'Poster': movie.get('thumbnail_url', ''),
        'Director': movie.get('director', 'N/A'),
        'Genre': movie.get('genre', 'N/A'),
        'Actors': movie.get('actors', 'N/A'),
        'Runtime': f"{movie.get('duration_minutes', 0)} min",
        'Plot': movie.get('description', 'N/A'),
        'imdbRating': str(movie.get('rating', 'N/A')),
    }
    
    return render(request, "catalog/detalhes.html", {"filme": filme_data})

