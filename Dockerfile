# Dockerfile
FROM python:3.13-slim

WORKDIR /project

# Системные зависимости
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Устанавливаем uv
RUN pip install uv

# Копируем проект
COPY . .

# Устанавливаем все зависимости, включая dev
RUN uv pip install -e . --system --group dev

# Открываем порт Django
EXPOSE 3000

# Команда по умолчанию — можно оставить pytest для CI
CMD ["uv", "run", "pytest", "-vv", "tests"]

