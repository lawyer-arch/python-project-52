### Hexlet тесты и статус линтера: [![Actions Status](https://github.com/lawyer-arch/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lawyer-arch/python-project-52/actions)

### SonarQube [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lawyer-arch_python-project-52&metric=alert_status)](https://sonarcloud.io/dashboard?id=lawyer-arch_python-project-52)


# Task Manager
**Менеджер задач (Task Manager)** — веб-приложение для управления задачами, аналог Redmine

___Демонстрация проекта по адресу:___ [Task manager на render.com](https://task-manager-dbze.onrender.com)

### *Описание проекта*

***Task Manager*** — это учебный проект, разработанный в рамках курса Hexlet Python-разработчик.

__Проект охватывает ключевые аспекты веб-разработки на Django:__

* Работа с моделями и ORM (One-to-Many, Many-to-Many)
* CRUD-операции с ресурсным роутингом
* Формы создания и редактирования сущностей
* Авторизация и аутентификация пользователей
* Фильтрация данных с помощью django-filter
* Отслеживание ошибок через Rollbar
* Тестирование приложения с использованием pytest

### Структура проекта

Основные модули приложения:

* users — управление пользователями (регистрация, вход, редактирование)
* tasks — создание и управление задачами
* statuses — статусы задач
* labels — метки для задач
* templates — HTML-шаблоны с Bootstrap
* tests — модульные тесты

### Развёртывание

**В продакшене используется:**
Gunicorn в качестве WSGI-сервера
PostgreSQL в качестве СУБД
Render.com как хостинг-платформа
Файл build.sh содержит команды для сборки и подготовки окружения.


### Технологический стек:

* Python 3.11+
* Django 5.2+
* PostgreSQL
* Bootstrap 5
* Gunicorn
* Rollbar
* Ruff — линтер
* Pytest / Pytest-Django — тестирование
* Render.com — деплой

### Установка и запуск
1. Клонирование репозитория:
```
git clone https://github.com/your-username/python-project-52.git
cd python-project-52
```

2. Установка зависимостей
Используется менеджер пакетов uv:
```
make install
```

3. Применение миграций:
```
make migrate
```

4. Запуск локального сервера:
```
make start
```

***Автор:***
Павел Аникин
Email: PavelDidko@gmail.com

### Учебный проект Hexlet

Проект создан в рамках курса «Python-разработчик» на [Хекслет](https://ru.hexlet.io/).
Цель — закрепить навыки создания полноценных Django-приложений с ORM, авторизацией, тестами и деплоем.