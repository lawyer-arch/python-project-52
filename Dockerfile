# Используем официальный Python 3.13
FROM python:3.13-slim

# Системные зависимости для Playwright и браузера
RUN apt-get update && apt-get install -y \
    curl wget gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libgtk-3-0 && \
    rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /project

# Копируем проект
COPY . .

# Создаем виртуальное окружение uv
RUN python -m venv .venv
ENV PATH="/project/.venv/bin:$PATH"

# Устанавливаем uv и зависимости из pyproject.toml
RUN pip install --upgrade pip
RUN pip install uv
RUN uv install --no-dev

# Устанавливаем зависимости для разработки и тестов
RUN uv install --dev

# Устанавливаем браузеры для Playwright
RUN python -m playwright install

# Команда по умолчанию для Hexlet
CMD ["uv", "run", "pytest", "-vv", "tests"]



