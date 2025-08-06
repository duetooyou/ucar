pip install -r requirements.txt
uvicorn main:app --reload

# Примеры curl запросов для Review Sentiment Analysis API

## Базовый URL
```
http://127.0.0.1:9000
```

## 1. Health Check
Проверка работоспособности сервиса:

```bash
curl -X GET "http://127.0.0.1:9000/"
```

**Ответ:**
```json
{
  "message": "Review Sentiment Analysis Service",
  "version": "1.0"
}
```

## 2. Создание отзывов (POST /reviews)

### Позитивный отзыв
```bash
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Отличный сервис, очень доволен!"}'
```

**Ответ:**
```json
{
  "id": 1,
  "text": "Отличный сервис, очень доволен!",
  "sentiment": "positive",
  "created_at": "2025-08-06T12:49:08.123456"
}
```

### Негативный отзыв
```bash
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ужасно работает, ненавижу этот сервис!"}'
```

**Ответ:**
```json
{
  "id": 2,
  "text": "Ужасно работает, ненавижу этот сервис!",
  "sentiment": "negative",
  "created_at": "2025-08-06T12:49:15.654321"
}
```

### Нейтральный отзыв
```bash
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Обычный сервис, ничего особенного"}'
```

**Ответ:**
```json
{
  "id": 3,
  "text": "Обычный сервис, ничего особенного",
  "sentiment": "neutral",
  "created_at": "2025-08-06T12:49:22.987654"
}
```

## 3. Получение отзывов (GET /reviews)

### Все отзывы
```bash
curl -X GET "http://127.0.0.1:9000/reviews"
```

### Только позитивные отзывы
```bash
curl -X GET "http://127.0.0.1:9000/reviews?sentiment=positive"
```

### Только негативные отзывы
```bash
curl -X GET "http://127.0.0.1:9000/reviews?sentiment=negative"
```

### Только нейтральные отзывы
```bash
curl -X GET "http://127.0.0.1:9000/reviews?sentiment=neutral"
```

**Пример ответа (список отзывов):**
```json
[
  {
    "id": 3,
    "text": "Обычный сервис, ничего особенного",
    "sentiment": "neutral",
    "created_at": "2025-08-06T12:49:22.987654"
  },
  {
    "id": 2,
    "text": "Ужасно работает, ненавижу этот сервис!",
    "sentiment": "negative",
    "created_at": "2025-08-06T12:49:15.654321"
  },
  {
    "id": 1,
    "text": "Отличный сервис, очень доволен!",
    "sentiment": "positive",
    "created_at": "2025-08-06T12:49:08.123456"
  }
]
```

## 4. Тестирование различных слов

### Тестирование позитивных слов
```bash
# "хорош"
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Хороший продукт"}'

# "люблю"
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Я люблю этот сайт"}'

# "супер"
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Супер качество!"}'
```

### Тестирование негативных слов
```bash
# "плохо"
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Работает плохо"}'

# "ненавижу"
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ненавижу эти глюки"}'

# "кошмар"
curl -X POST "http://127.0.0.1:9000/reviews" \
  -H "Content-Type: application/json" \
  -d '{"text": "Полный кошмар!"}'
```

## 5. Пакетное тестирование

Создать несколько отзывов подряд:

```bash
#!/bin/bash

# Позитивные отзывы
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Отличная работа!"}'
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Мне нравится интерфейс"}'
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Супер сервис!"}'

# Негативные отзывы
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Ужасно медленно"}'
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Не нравится дизайн"}'
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Плохо работает"}'

# Нейтральные отзывы
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Обычный сайт"}'
curl -X POST "http://127.0.0.1:9000/reviews" -H "Content-Type: application/json" -d '{"text": "Стандартный функционал"}'

# Получить все отзывы
curl -X GET "http://127.0.0.1:9000/reviews"

