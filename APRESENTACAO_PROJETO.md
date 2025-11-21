# 🎬 Netflix API - Apresentação do Projeto

## 📋 Visão Geral

API REST desenvolvida em **Django REST Framework** para gerenciamento de catálogo de filmes estilo Netflix, utilizando **armazenamento em JSON** ao invés de banco de dados tradicional.

---

## 🎯 Utilização

### Objetivo
Sistema de gerenciamento de filmes que permite:
- Consultar catálogo de filmes
- Adicionar novos filmes
- Atualizar informações
- Filtrar e buscar filmes
- Gerenciar filmes em destaque

### Público-Alvo
- Desenvolvedores que precisam de uma API de filmes
- Aplicações front-end que consomem dados de filmes
- Projetos educacionais de APIs REST

### Como Usar
1. Iniciar servidor: `python manage.py runserver`
2. Acessar endpoints via HTTP (Postman, navegador, aplicação)
3. Base URL: `http://127.0.0.1:8000/api/`

---

## ⚡ Funcionalidades

### 1. **CRUD Completo de Filmes**
- ✅ **Criar** novos filmes (POST)
- ✅ **Listar** todos os filmes (GET)
- ✅ **Buscar** filme por ID (GET)
- ✅ **Atualizar** filme completo (PUT)
- ✅ **Atualizar** filme parcial (PATCH)
- ✅ **Deletar** filme (DELETE)

### 2. **Filtros e Busca Avançada**
- 🔍 Busca por título ou descrição
- 🎭 Filtro por gênero
- ⭐ Filtro por rating mínimo
- 📅 Filtro por ano de lançamento
- ⭐ Filtro por filmes em destaque
- 📄 Paginação automática

### 3. **Endpoints Especializados**
- `/api/movies/genre/{genre}/` - Filmes por gênero
- `/api/movies/featured/` - Filmes em destaque

### 4. **Validação de Dados**
- Validação de rating (0-10)
- Validação de ano (1888-2100)
- Validação de duração (1-600 minutos)
- Validação de URLs
- Campos obrigatórios

---

## 🔧 Funcionamento Técnico

### Arquitetura

```
Cliente (Postman/Navegador)
    ↓ HTTP Request
Django REST Framework
    ↓
Views (views.py)
    ↓
Funções de Manipulação JSON
    ↓
Arquivo movies/data/movies.json
```

### Fluxo de Dados

1. **Requisição HTTP** chega ao Django
2. **URL Router** (`urls.py`) direciona para a view correta
3. **View** (`views.py`) processa a requisição:
   - Carrega dados do JSON (`load_movies()`)
   - Valida dados (`validate_movie()`)
   - Processa operação (CRUD)
   - Salva no JSON (`save_movies()`)
4. **Resposta JSON** retornada ao cliente

### Armazenamento

- **Formato**: JSON
- **Localização**: `movies/data/movies.json`
- **Estrutura**:
  ```json
  {
    "movies": [
      {
        "id": 1,
        "title": "...",
        "description": "...",
        ...
      }
    ]
  }
  ```

### Vantagens do JSON
- ✅ Simplicidade - sem necessidade de banco de dados
- ✅ Portabilidade - arquivo pode ser facilmente movido
- ✅ Legibilidade - fácil de ler e editar manualmente
- ✅ Desenvolvimento rápido - ideal para protótipos

---

## 💻 Codificação

### Estrutura do Projeto

```
netflix_project/
├── movies/                    # App principal
│   ├── views.py              # Lógica de negócio e endpoints
│   ├── urls.py                # Roteamento de URLs
│   ├── apps.py                # Configuração do app
│   └── data/
│       └── movies.json        # Armazenamento de dados
├── netflix_project/           # Configuração Django
│   ├── settings.py           # Configurações do projeto
│   └── urls.py                # URLs principais
└── manage.py                  # Script de gerenciamento Django
```

### Componentes Principais

#### 1. **views.py** - Lógica Principal
```python
# Funções auxiliares
- load_movies()          # Carrega filmes do JSON
- save_movies()          # Salva filmes no JSON
- validate_movie()       # Valida dados do filme
- paginate_response()    # Aplica paginação
- find_movie()          # Encontra filme por ID

# Endpoints
- get_all_movies()      # GET/POST /api/movies/
- movie_detail()         # GET/PUT/PATCH/DELETE /api/movies/{id}/
- get_movies_by_genre()  # GET /api/movies/genre/{genre}/
- get_featured_movies()  # GET /api/movies/featured/
```

#### 2. **urls.py** - Roteamento
```python
urlpatterns = [
    path('movies/', views.get_all_movies),
    path('movies/<int:pk>/', views.movie_detail),
    path('movies/genre/<str:genre>/', views.get_movies_by_genre),
    path('movies/featured/', views.get_featured_movies),
]
```

#### 3. **settings.py** - Configuração
- Django REST Framework configurado
- Idioma: Português-BR
- Timezone: America/Sao_Paulo
- SQLite em memória (para apps Django que precisam)

### Tecnologias Utilizadas

- **Python 3.x** - Linguagem de programação
- **Django 5.2.8** - Framework web
- **Django REST Framework 3.15.2** - Framework para APIs REST
- **JSON** - Armazenamento de dados

### Padrões de Código

1. **Separação de Responsabilidades**
   - Funções auxiliares separadas da lógica de endpoints
   - Validação isolada em função própria

2. **Código Limpo**
   - Funções pequenas e focadas
   - Nomes descritivos
   - Comentários em português

3. **Tratamento de Erros**
   - Validação antes de processar
   - Mensagens de erro claras
   - Status HTTP apropriados

### Exemplo de Código - Criar Filme

```python
@api_view(['GET', 'POST'])
def get_all_movies(request):
    if request.method == 'POST':
        # 1. Validar dados
        errors = validate_movie(data, is_update=False)
        if errors:
            return Response(errors, status=400)
        
        # 2. Carregar filmes existentes
        movies = load_movies()
        
        # 3. Gerar novo ID
        new_id = max((m.get('id', 0) for m in movies), default=0) + 1
        
        # 4. Criar novo filme
        new_movie = {...}
        movies.append(new_movie)
        
        # 5. Salvar no JSON
        save_movies(movies)
        
        # 6. Retornar resposta
        return Response(new_movie, status=201)
```

---

## 📊 Estatísticas do Projeto

- **Linhas de código**: ~250 linhas
- **Endpoints**: 4 principais + variações
- **Arquivos principais**: 3 (views.py, urls.py, settings.py)
- **Dependências**: 2 (Django, DRF)
- **Tempo de resposta**: < 100ms (dados em memória)

---

## 🎓 Aprendizados e Diferenciais

### Diferenciais do Projeto
1. **Simplicidade** - Sem banco de dados, fácil de entender
2. **Completo** - CRUD completo com validações
3. **Filtros Avançados** - Múltiplas formas de buscar
4. **Português-BR** - Totalmente traduzido
5. **Código Limpo** - Fácil manutenção

### Conceitos Aplicados
- RESTful API
- Validação de dados
- Paginação
- Filtros e busca
- Tratamento de erros HTTP
- Serialização JSON

---

## 🚀 Demonstração Rápida

### Exemplo 1: Listar Filmes
```
GET http://127.0.0.1:8000/api/movies/
```

### Exemplo 2: Criar Filme
```
POST http://127.0.0.1:8000/api/movies/
Body: {
  "title": "Novo Filme",
  "description": "...",
  ...
}
```

### Exemplo 3: Filtrar por Gênero
```
GET http://127.0.0.1:8000/api/movies/genre/Ação/
```

---

## 📝 Conclusão

Projeto desenvolvido para demonstrar:
- Criação de APIs REST com Django
- Gerenciamento de dados em JSON
- Validação e tratamento de erros
- Filtros e busca avançada
- Boas práticas de código Python

**Ideal para**: Aprendizado, protótipos rápidos e projetos que não requerem banco de dados complexo.

---

## 🔗 Recursos Adicionais

- Documentação completa: `TESTE_POSTMAN.md`
- Guia de inicialização: `INICIAR_SERVIDOR.md`
- Resumo de testes: `RESUMO_TESTES.md`

---

**Desenvolvido com Django REST Framework** 🐍✨



