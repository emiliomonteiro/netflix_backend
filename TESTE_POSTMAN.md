# Guia de Testes - API Netflix no Postman

## 🚀 Iniciar o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://127.0.0.1:8000`

---

## 📋 Endpoints Disponíveis

### Base URL
```
http://127.0.0.1:8000/api
```

---

## 🎬 1. Listar Todos os Filmes (GET)

**URL:** `GET http://127.0.0.1:8000/api/movies/`

**Query Parameters (opcionais):**
- `search` - Busca por título ou descrição
- `genre` - Filtrar por gênero
- `min_rating` - Rating mínimo (ex: 8.5)
- `year` - Filtrar por ano
- `featured` - Filtrar por featured (true/false)
- `page` - Número da página
- `page_size` - Itens por página (máx 100)

**Exemplos:**
```
GET http://127.0.0.1:8000/api/movies/
GET http://127.0.0.1:8000/api/movies/?search=matrix
GET http://127.0.0.1:8000/api/movies/?genre=Ação&min_rating=8
GET http://127.0.0.1:8000/api/movies/?featured=true
GET http://127.0.0.1:8000/api/movies/?page=1&page_size=5
```

**Resposta Esperada:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Matrix",
      "description": "...",
      "genre": "Ficção Científica",
      "release_year": 1999,
      "duration_minutes": 136,
      "rating": "8.7",
      "thumbnail_url": "https://example.com/matrix-thumb.jpg",
      "video_url": "https://example.com/matrix-video.mp4",
      "is_featured": true,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

---

## ➕ 2. Criar Novo Filme (POST)

**URL:** `POST http://127.0.0.1:8000/api/movies/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "title": "Interestelar",
  "description": "Uma equipe de exploradores viaja através de um buraco de minhoca no espaço em uma tentativa de garantir a sobrevivência da humanidade.",
  "genre": "Ficção Científica",
  "release_year": 2014,
  "duration_minutes": 169,
  "rating": 8.6,
  "thumbnail_url": "https://example.com/interstellar-thumb.jpg",
  "video_url": "https://example.com/interstellar-video.mp4",
  "is_featured": true
}
```

**Resposta Esperada (201 Created):**
```json
{
  "id": 4,
  "title": "Interestelar",
  "description": "...",
  "genre": "Ficção Científica",
  "release_year": 2014,
  "duration_minutes": 169,
  "rating": 8.6,
  "thumbnail_url": "https://example.com/interstellar-thumb.jpg",
  "video_url": "https://example.com/interstellar-video.mp4",
  "is_featured": true,
  "created_at": "2024-11-15T12:00:00",
  "updated_at": "2024-11-15T12:00:00"
}
```

---

## 🔍 3. Buscar Filme por ID (GET)

**URL:** `GET http://127.0.0.1:8000/api/movies/{id}/`

**Exemplo:**
```
GET http://127.0.0.1:8000/api/movies/1/
```

**Resposta Esperada:**
```json
{
  "id": 1,
  "title": "Matrix",
  "description": "...",
  "genre": "Ficção Científica",
  "release_year": 1999,
  "duration_minutes": 136,
  "rating": "8.7",
  "thumbnail_url": "https://example.com/matrix-thumb.jpg",
  "video_url": "https://example.com/matrix-video.mp4",
  "is_featured": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

## ✏️ 4. Atualizar Filme Completo (PUT)

**URL:** `PUT http://127.0.0.1:8000/api/movies/{id}/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON) - Todos os campos obrigatórios:**
```json
{
  "title": "Matrix Reloaded",
  "description": "Neo descobre mais sobre a Matrix e precisa enfrentar novos desafios.",
  "genre": "Ficção Científica",
  "release_year": 2003,
  "duration_minutes": 138,
  "rating": 7.2,
  "thumbnail_url": "https://example.com/matrix2-thumb.jpg",
  "video_url": "https://example.com/matrix2-video.mp4",
  "is_featured": false
}
```

**Exemplo:**
```
PUT http://127.0.0.1:8000/api/movies/1/
```

---

## 🔄 5. Atualizar Filme Parcial (PATCH)

**URL:** `PATCH http://127.0.0.1:8000/api/movies/{id}/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON) - Apenas campos a atualizar:**
```json
{
  "rating": 9.0,
  "is_featured": true
}
```

**Exemplo:**
```
PATCH http://127.0.0.1:8000/api/movies/1/
```

---

## 🗑️ 6. Deletar Filme (DELETE)

**URL:** `DELETE http://127.0.0.1:8000/api/movies/{id}/`

**Exemplo:**
```
DELETE http://127.0.0.1:8000/api/movies/3/
```

**Resposta Esperada:** `204 No Content` (sem corpo)

---

## 🎭 7. Filtrar por Gênero (GET)

**URL:** `GET http://127.0.0.1:8000/api/movies/genre/{genre}/`

**Exemplos:**
```
GET http://127.0.0.1:8000/api/movies/genre/Ação/
GET http://127.0.0.1:8000/api/movies/genre/Drama/
GET http://127.0.0.1:8000/api/movies/genre/Ficção Científica/
```

**Resposta Esperada:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "genre": "Ação",
  "results": [...]
}
```

---

## ⭐ 8. Listar Filmes em Destaque (GET)

**URL:** `GET http://127.0.0.1:8000/api/movies/featured/`

**Resposta Esperada:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Matrix",
      ...
    },
    {
      "id": 2,
      "title": "O Poderoso Chefão",
      ...
    }
  ]
}
```

---

## ⚠️ Validações e Erros

### Campos Obrigatórios (POST/PUT):
- `title`
- `description`
- `genre`
- `release_year`
- `duration_minutes`
- `rating`
- `thumbnail_url`
- `video_url`

### Regras de Validação:
- **rating**: Deve estar entre 0 e 10
- **release_year**: Deve estar entre 1888 e 2100
- **duration_minutes**: Deve ser maior que 0 e menor que 600
- **URLs**: Devem ter formato válido

### Exemplo de Erro (400 Bad Request):
```json
{
  "rating": ["Nota deve estar entre 0 e 10"],
  "release_year": ["Este campo é obrigatório."]
}
```

### Exemplo de Erro (404 Not Found):
```json
{
  "error": "Filme não encontrado"
}
```

---

## 📝 Coleção Postman

### Importar no Postman:
1. Abra o Postman
2. Clique em "Import"
3. Crie uma nova coleção chamada "Netflix API"
4. Adicione os endpoints acima

### Variáveis de Ambiente (Opcional):
Crie um ambiente no Postman com:
- `base_url`: `http://127.0.0.1:8000/api`

Então use: `{{base_url}}/movies/`

---

## ✅ Checklist de Testes

- [ ] GET todos os filmes
- [ ] GET com filtros (search, genre, min_rating, year, featured)
- [ ] GET com paginação
- [ ] POST criar novo filme
- [ ] POST com dados inválidos (testar validações)
- [ ] GET filme por ID
- [ ] GET filme inexistente (404)
- [ ] PUT atualizar filme completo
- [ ] PATCH atualizar filme parcial
- [ ] DELETE remover filme
- [ ] GET por gênero
- [ ] GET filmes em destaque

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### Erro: "CSRF verification failed"
- No Postman, desabilite CSRF ou adicione header:
```
X-CSRFToken: <token>
```

### Servidor não inicia
```bash
python manage.py check
```

---

**Boa sorte com os testes! 🚀**

