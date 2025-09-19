# FastAPI-base-app

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/USERNAME/REPO.git
cd REPO
```

### 2. Установка зависимостей
```bash
poetry install
```

### 3. Настройка окружения
```bash
cp fastapi-application/.env.template fastapi-application/.env
```
Отредактируйте `.env` и `docker-compose.yml`, указав свои значения.

### 4. Локальная работа
Активация виртуального окружения:
```bash
source $(poetry env info --path)/bin/activate
```

В IDE (PyCharm/VScode) укажите интерпретатор из poetry-окружения:
```bash
poetry env info --path
```
Пометьте `fastapi-application` как **Sources Root** для корректных импортов.
### 5. Запуск в Docker
```bash
docker-compose up --build
```

### 6. Миграции
```bash
cd fastapi-application
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### 7. Запуск приложения
```bash
cd fastapi-application
uvicorn fastapi-application.main:main_app --reload
```

Приложение будет доступно по адресу:  
👉 http://localhost:8000/docs

---

✅ Всё готово к работе.
