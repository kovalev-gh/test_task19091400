from core.gunicorn.logger import GunicornLogger

# Адрес и порт, которые будет слушать Gunicorn
bind = "0.0.0.0:8000"

# Количество воркеров (обычно = число CPU * 2)
workers = 4

# Таймаут соединения (в секундах)
timeout = 120

# Уровень логирования
loglevel = "info"

# Класс логгера
logger_class = GunicornLogger

# Класс воркеров (Uvicorn для FastAPI/ASGI)
worker_class = "uvicorn.workers.UvicornWorker"

# Логи в stdout/stderr (удобно для Docker)
accesslog = "-"
errorlog = "-"
