FROM python:3.12-slim

# Установим системные зависимости
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установим Poetry
RUN pip install poetry

# Скопируем pyproject и lock-файл
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей (только основные, без dev)
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

# Копируем весь проект
COPY . /app

# Ставим рабочую директорию внутрь fastapi-application
WORKDIR /app/fastapi-application

# Команда по умолчанию
CMD alembic upgrade head && gunicorn core.gunicorn.application:app -c core/gunicorn/app_options.py
