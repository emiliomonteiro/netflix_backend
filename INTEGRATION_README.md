# Integração de Projetos Netflix

Este projeto integra duas funcionalidades:
1. **API REST** (`/api/`) - Gerenciamento CRUD de filmes via JSON
2. **Catálogo Web** (`/`) - Interface web estilo Netflix com autenticação

## Estrutura Integrada

```
netflix_project/
├── movies/              # App da API REST (JSON storage)
│   ├── views.py         # Endpoints REST API
│   └── data/
│       └── movies.json  # Armazenamento JSON compartilhado
├── catalog/             # App do catálogo web (copiado de backend_django/netflix)
│   ├── views.py         # Views web (lê do JSON)
│   ├── templates/       # Templates HTML
│   └── management/
│       └── commands/
│           └── sync_omdb.py  # Comando de sincronização OMDB
└── netflix_project/     # Configurações do projeto
    ├── settings.py      # Configurações unificadas
    └── urls.py          # Roteamento unificado
```

## Funcionalidades

### 1. API REST (`/api/movies/`)
- CRUD completo de filmes
- Filtros: search, genre, min_rating, year, featured
- Paginação
- Armazena dados em `movies/data/movies.json`

### 2. Catálogo Web (`/`)
- Interface web estilo Netflix
- Autenticação obrigatória (login em `/accounts/login/`)
- Exibe filmes sincronizados do OMDB
- Detalhes dos filmes

### 3. Sincronização OMDB
- Comando de sincronização que busca dados da API OMDB
- Alimenta o arquivo JSON compartilhado
- Preserva filmes criados manualmente via API

## Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Sincronizar Filmes do OMDB
```bash
python manage.py sync_omdb
```

Este comando:
- Busca 19 filmes populares da API OMDB
- Adiciona/atualiza no arquivo `movies/data/movies.json`
- Preserva filmes existentes criados manualmente

### 3. Iniciar Servidor
```bash
python manage.py runserver
```

### 4. Acessar

- **Catálogo Web**: http://127.0.0.1:8000/ (requer login)
- **API REST**: http://127.0.0.1:8000/api/movies/
- **Admin**: http://127.0.0.1:8000/admin/

## Fluxo de Dados

```
OMDB API → sync_omdb.py → movies.json ← API REST / Catálogo Web
```

1. **Sincronização OMDB**: O comando `sync_omdb` busca dados da API OMDB e salva no JSON
2. **API REST**: Lê/escreve diretamente no JSON
3. **Catálogo Web**: Lê do JSON para exibir filmes

## Configuração

### Chave da API OMDB

A chave padrão está em `netflix_project/settings.py`:
```python
OMDB_API_KEY = 'bd8a882'
```

Para usar uma chave diferente:
```bash
python manage.py sync_omdb --api-key SUA_CHAVE
```

Ou configure via variável de ambiente (recomendado para produção).

## Criar Usuário para Login

```bash
python manage.py createsuperuser
```

Ou via shell do Django:
```python
from django.contrib.auth.models import User
User.objects.create_user('username', 'email@example.com', 'password')
```

## Estrutura do JSON

O arquivo `movies/data/movies.json` armazena todos os filmes:

```json
{
  "movies": [
    {
      "id": 1,
      "title": "The Avengers",
      "description": "...",
      "genre": "Action",
      "release_year": 2012,
      "duration_minutes": 143,
      "rating": 8.0,
      "thumbnail_url": "https://...",
      "video_url": "",
      "is_featured": false,
      "imdb_id": "tt0848228",
      "director": "Joss Whedon",
      "actors": "...",
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-01T00:00:00"
    }
  ]
}
```

## Notas Importantes

1. **Filmes OMDB vs Manuais**: 
   - Filmes sincronizados do OMDB têm `imdb_id`
   - Filmes criados via API podem não ter `imdb_id`
   - O catálogo web exibe apenas filmes com `imdb_id`

2. **Sincronização Periódica**:
   - Execute `sync_omdb` periodicamente para atualizar dados
   - O comando atualiza filmes existentes se já tiverem o mesmo `imdb_id`

3. **Preservação de Dados**:
   - Filmes criados manualmente via API são preservados
   - Apenas filmes com `imdb_id` correspondente são atualizados pelo sync

## Endpoints da API

- `GET /api/movies/` - Lista filmes (com filtros)
- `POST /api/movies/` - Cria filme
- `GET /api/movies/{id}/` - Detalhes do filme
- `PUT /api/movies/{id}/` - Atualiza filme completo
- `PATCH /api/movies/{id}/` - Atualiza filme parcial
- `DELETE /api/movies/{id}/` - Remove filme
- `GET /api/movies/genre/{genre}/` - Filmes por gênero
- `GET /api/movies/featured/` - Filmes em destaque

## Rotas Web

- `/` - Catálogo de filmes (requer login)
- `/filme/<imdb_id>/` - Detalhes do filme
- `/accounts/login/` - Página de login
- `/logout/` - Logout

