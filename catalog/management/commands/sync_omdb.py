import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from datetime import datetime

# Lista de IDs IMDB para sincronizar (copiada do projeto original)
LISTA_IMDB = [
    "tt0848228",  # The Avengers
    "tt0816692",  # Interstellar
    "tt0133093",  # The Matrix
    "tt1375666",  # Inception
    "tt4154796",  # Avengers: Endgame
    "tt2488496",  # Star Wars: The Force Awakens
    "tt4154756",  # Avengers: Infinity War
    "tt1877830",  # The Batman
    "tt0499549",  # Avatar
    "tt1630029",  # Avatar: The Way of Water
    "tt0468569",  # The Dark Knight
    "tt2975590",  # Batman v Superman: Dawn of Justice
    "tt3606756",  # Jungle Book
    "tt0381061",  # Casino Royale
    "tt0167260",  # The Lord of the Rings: The Return of the King
    "tt0120737",  # The Lord of the Rings: The Fellowship of the Ring
    "tt3749900",  # The Nice Guys
    "tt0107290",  # Jurassic Park
    "tt0110413",  # Léon: The Professional
]

JSON_FILE_PATH = os.path.join(settings.BASE_DIR, 'movies', 'data', 'movies.json')
OMDB_API_KEY = getattr(settings, 'OMDB_API_KEY', 'bd8a882')


class Command(BaseCommand):
    help = 'Sincroniza filmes da API OMDB para o arquivo JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='Chave da API OMDB (ou use OMDB_API_KEY nas settings)',
        )

    def handle(self, *args, **options):
        api_key = options.get('api_key') or OMDB_API_KEY
        
        self.stdout.write(self.style.SUCCESS('Iniciando sincronização OMDB...'))
        
        # Carregar filmes existentes
        movies = self.load_movies()
        existing_imdb_ids = {m.get('imdb_id') for m in movies if m.get('imdb_id')}
        
        synced_count = 0
        updated_count = 0
        error_count = 0
        
        for imdb_id in LISTA_IMDB:
            try:
                # Buscar dados do OMDB
                url = f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                omdb_data = response.json()
                
                if omdb_data.get('Response') == 'False':
                    self.stdout.write(self.style.WARNING(f'Filme {imdb_id} não encontrado na OMDB'))
                    error_count += 1
                    continue
                
                # Converter dados OMDB para formato do JSON
                movie_data = self.convert_omdb_to_movie(omdb_data)
                
                # Verificar se já existe
                existing_index = None
                for i, m in enumerate(movies):
                    if m.get('imdb_id') == imdb_id:
                        existing_index = i
                        break
                
                if existing_index is not None:
                    # Atualizar filme existente
                    movies[existing_index].update(movie_data)
                    movies[existing_index]['updated_at'] = datetime.now().isoformat()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Atualizado: {movie_data["title"]}'))
                else:
                    # Adicionar novo filme
                    new_id = max((m.get('id', 0) for m in movies), default=0) + 1
                    movie_data['id'] = new_id
                    movie_data['created_at'] = datetime.now().isoformat()
                    movie_data['updated_at'] = datetime.now().isoformat()
                    movies.append(movie_data)
                    synced_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Adicionado: {movie_data["title"]}'))
                    
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Erro ao buscar {imdb_id}: {str(e)}'))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao processar {imdb_id}: {str(e)}'))
                error_count += 1
        
        # Salvar filmes atualizados
        if self.save_movies(movies):
            self.stdout.write(self.style.SUCCESS(
                f'\nSincronização concluída!\n'
                f'  - Novos filmes: {synced_count}\n'
                f'  - Filmes atualizados: {updated_count}\n'
                f'  - Erros: {error_count}\n'
                f'  - Total de filmes no JSON: {len(movies)}'
            ))
        else:
            self.stdout.write(self.style.ERROR('Erro ao salvar filmes no JSON'))

    def load_movies(self):
        """Carrega filmes do arquivo JSON"""
        try:
            if os.path.exists(JSON_FILE_PATH):
                with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                    return json.load(file).get('movies', [])
            return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_movies(self, movies):
        """Salva filmes no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)
            with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump({'movies': movies}, file, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao salvar: {str(e)}'))
            return False

    def convert_omdb_to_movie(self, omdb_data):
        """Converte dados da API OMDB para formato do JSON"""
        # Extrair duração em minutos do runtime (ex: "136 min" -> 136)
        runtime_str = omdb_data.get('Runtime', '0 min')
        duration_minutes = 0
        try:
            duration_minutes = int(runtime_str.replace(' min', '').strip())
        except (ValueError, AttributeError):
            pass
        
        # Extrair ano do release_year
        release_year = 0
        try:
            release_year = int(omdb_data.get('Year', '0').split('–')[0].strip())
        except (ValueError, AttributeError):
            pass
        
        # Extrair rating (IMDB rating como float)
        rating = 0.0
        try:
            rating = float(omdb_data.get('imdbRating', '0') or '0')
        except (ValueError, AttributeError):
            pass
        
        return {
            'title': omdb_data.get('Title', ''),
            'description': omdb_data.get('Plot', ''),
            'genre': omdb_data.get('Genre', ''),
            'release_year': release_year,
            'duration_minutes': duration_minutes,
            'rating': rating,
            'thumbnail_url': omdb_data.get('Poster', ''),
            'video_url': '',  # OMDB não fornece video_url
            'is_featured': False,  # Pode ser configurado manualmente depois
            'imdb_id': omdb_data.get('imdbID', ''),
            # Campos adicionais do OMDB para uso futuro
            'director': omdb_data.get('Director', ''),
            'actors': omdb_data.get('Actors', ''),
            'writer': omdb_data.get('Writer', ''),
            'language': omdb_data.get('Language', ''),
            'country': omdb_data.get('Country', ''),
            'awards': omdb_data.get('Awards', ''),
            'metascore': omdb_data.get('Metascore', ''),
            'imdb_votes': omdb_data.get('imdbVotes', ''),
        }

