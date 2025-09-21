# Test_task19091400

## ⚙️ Настройка окружения

```bash
cp fastapi-application/.env.example fastapi-application/.env
```

Отредактируйте файлы:
- `fastapi-application/.env`
- `docker-compose.yml`

Укажите свои значения (БД, секреты, порты).

## 🚀 Запуск через Docker

```bash
docker compose up -d --build
```

Миграции применяются автоматически.  
Создаётся пользователь по умолчанию:

```json
{
  "email": "admin@example.com",
  "password": "admin"
}
```

Приложение будет доступно по адресу:  
👉 [http://127.0.0.1/docs](http://127.0.0.1/docs)

## 🧪 Запуск тестов

Из корня проекта выполните:

```bash
poetry run pytest -v
```

---

✅ Всё готово к работе!
