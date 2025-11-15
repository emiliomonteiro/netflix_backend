# 🚀 Como Iniciar o Servidor

## 1. Verificar Dependências

```bash
pip install -r requirements.txt
```

## 2. Verificar Configuração

```bash
python manage.py check
```

## 3. Iniciar o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: **http://127.0.0.1:8000**

## 4. Testar no Navegador

Abra no navegador:
```
http://127.0.0.1:8000/api/movies/
```

Você deve ver uma resposta JSON com os filmes.

## 5. Testar no Postman

Consulte o arquivo `TESTE_POSTMAN.md` para instruções detalhadas.

---

## ⚠️ Nota sobre CSRF

Para requisições POST/PUT/PATCH/DELETE no Postman, você pode precisar:

1. **Opção 1**: Desabilitar CSRF temporariamente (apenas para desenvolvimento)
   - Adicione `@csrf_exempt` nas views (não recomendado para produção)

2. **Opção 2**: Usar o Postman com configuração adequada
   - O Django REST Framework geralmente funciona sem CSRF para APIs
   - Se necessário, adicione header: `X-CSRFToken: <token>`

3. **Opção 3**: Usar `curl` ou ferramentas similares

---

## 📝 Exemplo de Teste Rápido

### Teste GET (no navegador ou Postman):
```
GET http://127.0.0.1:8000/api/movies/
```

### Teste POST (no Postman):
```
POST http://127.0.0.1:8000/api/movies/
Content-Type: application/json

{
  "title": "Teste",
  "description": "Descrição teste",
  "genre": "Ação",
  "release_year": 2024,
  "duration_minutes": 120,
  "rating": 8.5,
  "thumbnail_url": "https://example.com/thumb.jpg",
  "video_url": "https://example.com/video.mp4",
  "is_featured": false
}
```

---

## 🐛 Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### Erro: "CSRF verification failed"
- No Postman, adicione no Headers:
  - `X-CSRFToken: <obter token do cookie>`
- Ou use a extensão Postman Interceptor

### Porta 8000 já em uso
```bash
python manage.py runserver 8001
```

---

**Pronto para testar! 🎬**

