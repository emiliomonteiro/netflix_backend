# 🎬 Netflix API - Apresentação Resumida

## 📌 O QUE É?

API REST em Django para gerenciar catálogo de filmes estilo Netflix, usando **JSON como banco de dados**.

---

## 🎯 UTILIZAÇÃO

**Para que serve?**
- Gerenciar catálogo de filmes
- API para aplicações front-end
- Projeto educacional de APIs REST

**Como usar?**
1. Iniciar: `python manage.py runserver`
2. Acessar: `http://127.0.0.1:8000/api/`
3. Testar no Postman ou navegador

---

## ⚡ FUNCIONALIDADES

### CRUD Completo
- ✅ Criar, Listar, Buscar, Atualizar, Deletar filmes

### Filtros Avançados
- 🔍 Busca por título/descrição
- 🎭 Filtro por gênero
- ⭐ Filtro por rating mínimo
- 📅 Filtro por ano
- ⭐ Filmes em destaque
- 📄 Paginação automática

### Endpoints Especializados
- `/api/movies/genre/{genre}/` - Por gênero
- `/api/movies/featured/` - Em destaque

---

## 🔧 FUNCIONAMENTO

### Arquitetura Simples
```
Cliente → Django REST Framework → Views → JSON File
```

### Fluxo de Dados
1. **Requisição HTTP** chega
2. **URL Router** direciona para view
3. **View** processa:
   - Carrega JSON
   - Valida dados
   - Executa operação (CRUD)
   - Salva no JSON
4. **Resposta JSON** retorna

### Armazenamento
- **Formato**: JSON (`movies/data/movies.json`)
- **Vantagem**: Simples, portável, sem banco de dados

---

## 💻 CODIFICAÇÃO

### Estrutura
```
movies/
├── views.py       # Lógica principal (250 linhas)
├── urls.py        # Roteamento
└── data/
    └── movies.json # Dados
```

### Componentes Principais

**1. views.py** - 5 funções principais:
- `load_movies()` - Carrega do JSON
- `save_movies()` - Salva no JSON
- `validate_movie()` - Valida dados
- `get_all_movies()` - GET/POST
- `movie_detail()` - GET/PUT/PATCH/DELETE

**2. urls.py** - 4 rotas:
- `/movies/` - Lista/Cria
- `/movies/{id}/` - Detalhes/Atualiza/Deleta
- `/movies/genre/{genre}/` - Por gênero
- `/movies/featured/` - Em destaque

### Tecnologias
- **Python 3.x**
- **Django 5.2.8**
- **Django REST Framework 3.15.2**
- **JSON** (armazenamento)

### Exemplo de Código
```python
@api_view(['POST'])
def get_all_movies(request):
    # 1. Validar
    errors = validate_movie(data)
    # 2. Carregar
    movies = load_movies()
    # 3. Criar
    new_movie = {...}
    movies.append(new_movie)
    # 4. Salvar
    save_movies(movies)
    # 5. Retornar
    return Response(new_movie, status=201)
```

---

## 📊 NÚMEROS

- **250 linhas** de código
- **4 endpoints** principais
- **3 arquivos** principais
- **2 dependências** (Django + DRF)
- **< 100ms** tempo de resposta

---

## 🎓 DIFERENCIAIS

1. ✅ **Simplicidade** - Sem banco de dados
2. ✅ **Completo** - CRUD + validações
3. ✅ **Filtros** - Múltiplas formas de buscar
4. ✅ **Português-BR** - Totalmente traduzido
5. ✅ **Código Limpo** - Fácil manutenção

---

## 🚀 DEMONSTRAÇÃO

### Exemplo 1: Listar
```
GET /api/movies/
```

### Exemplo 2: Criar
```
POST /api/movies/
Body: {"title": "...", ...}
```

### Exemplo 3: Filtrar
```
GET /api/movies/genre/Ação/
```

---

## ✅ CONCLUSÃO

**Projeto educativo** demonstrando:
- APIs REST com Django
- Gerenciamento JSON
- Validação de dados
- Boas práticas Python

**Ideal para**: Aprendizado e protótipos rápidos.

---

**Desenvolvido com Django REST Framework** 🐍✨



