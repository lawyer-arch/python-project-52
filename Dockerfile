# Dockerfile
FROM python:3.13-slim

WORKDIR /project

# Системные зависимости (PostgreSQL и сборка пакетов)
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Устанавливаем uv
RUN pip install uv

# Копируем проект
COPY . .

# Устанавливаем зависимости через uv
RUN uv pip install --group dev --system -e .

# Открываем порт Django
EXPOSE 3000

# Команда по умолчанию для контейнера
CMD ["uv", "run", "pytest", "-vv", "tests"]
