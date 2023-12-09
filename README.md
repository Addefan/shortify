# Shortify

## [Описание](VISION.md)

## [Схема базы данных](schema.png)

## Локальный запуск проекта

1. `python -m venv venv` - создание виртуального окружения
2. `source venv/bin/activate` - вход в виртуальное окружение
3. `pip install -r requirements.txt` - установка зависимостей
4. `python manage.py migrate` - применение миграций
5. `python manage.py runserver` - запуск сервера