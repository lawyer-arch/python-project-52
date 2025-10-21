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
	python manage.py makemigrations
	python manage.py migrate

render-start:
	gunicorn task_manager.wsgi:application


trans:
	# Компилируем только свои .po файлы в каталоге проекта, игнорируя .venv
	find ./locale -name "*.po" | while read po; do \
		dir=$$(dirname $$po); \
		msgfmt $$po -o $$dir/$$(basename $$po .po).mo || true; \
	done
