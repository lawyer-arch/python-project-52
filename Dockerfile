FROM python:3.13

WORKDIR /project

# Копируем pyproject.toml для кеша слоёв
COPY pyproject.toml poetry.lock* ./

# Обновляем pip и устанавливаем зависимости
RUN python -m pip install --upgrade pip
RUN pip install pytest pytest-django build .

# Копируем весь проект
COPY . .

# Переменные окружения
ENV VIRTUAL_ENV=/project/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1






