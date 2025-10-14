.PHONY: lint test start

# Запуск приложения
start:
	python manage.py runserver

# Запуск проверки стиля кода с помощью Ruff
lint:
	ruff check .

lint-fix:
	ruff check . --fix

# Тесты (можно расширить позже)
test:
	pytest --ds=task_manager.settings

build:
	./build.sh

install:
	uv sync

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

render-start:
	gunicorn task_manager.wsgi:application

trans:
	python manage.py makemessages -l ru
	python manage.py compilemessages
