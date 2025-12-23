# Geo Backend — Django + GeoDjango

Backend-приложение на Django для работы с географическими точками и сообщениями пользователей.  
Предоставляет REST API для создания гео-точек, сообщений и поиска контента в заданном радиусе от координат.

---

## Возможности

- Создание точек на карте  
- Создание сообщений, привязанных к точкам  
- Поиск точек в заданном радиусе  
- Поиск сообщений в заданном радиусе

---

## Технологический стек

- Python 3.10+
- Django 5.x
- Django REST Framework (DRF)
- GeoDjango
- PostgreSQL + PostGIS
- pytest / pytest-django

---

## Установка и запуск

#### 1. Клонирование проекта

```bash
git clone https://github.com/phentalex/geo_backend
cd geo_backend
```

#### 2. Создание виртуального окружения

```bash
python -m venv venv
```

Активация **Linux / macOS**:
```bash
source venv/bin/activate
```

Активация **Windows**:
```bash
source venv/Scripts/activate
```

#### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## Настройка базы данных (PostgreSQL + PostGIS)

#### 1. Установить PostgreSQL
#### 2. Установить расширение PostGIS
#### 3. Установить GDAL и GEOS (обязательно для GeoDjango)
### Windows
1. Скачать установщик:
  *https://trac.osgeo.org/osgeo4w/*
2. Запустить osgeo4w-setup-x86_64.exe
3. В режиме установки выбрать:
  - Advanced Install
  - Раздел Libs
    - `gdal`
    - `geos`
4. Дождаться окончания установки

По умолчанию библиотеки будут установлены в:
```sql
C:\Users\<USER>\AppData\Local\Programs\OSGeo4W\bin\
```

### для Linux / macOS
```bash
sudo apt install gdal-bin libgdal-dev libgeos-dev
```
или
```bash
brew install gdal geos
```
В этих системах `GDAL_LIBRARY_PATH` и `GEOS_LIBRARY_PATH` обычно не требуются.

#### 4. Создать базу данных:

```bash
CREATE DATABASE geo_points_db;
```

#### 5. Включить PostGIS:

```bash
CREATE EXTENSION postgis;
```

#### 6. Создать .env

Пример:
```bash
DEBUG=1
SECRET_KEY=<secret_key>
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=geo_points_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

TIME_ZONE=Europe/Moscow
LANGUAGE_CODE=ru-ru

GDAL_LIBRARY_PATH=<path_to_dgal.dll>
GEOS_LIBRARY_PATH=<path_to_geos.dll>
```

---

## Запуск приложения
```bash
python manage.py migrate
python manage.py runserver
```
### После запуска сервер будет доступен по адресу:
**http://127.0.0.1:8000/**

---

## Авторизация

### Все API-эндпоинты требуют авторизации.

#### Для тестирования можно:
- создать супер пользователя и авторизоваться в /admin/ или Basic Auth(Postman)
  ```bash
  python manage.py createsuperuser
  ```
- создать пользователя через Django Admin (/admin/)

---

## API эндпоинты
### Создание географической точки

POST `/api/points/`

Тело запроса:
```json
{
  "title": "Моё место",
  "longitude": 37.61,
  "latitude": 55.75
}
```
Ответ:
```json
{
  "id": 1,
  "title": "Моё место",
  "location": "SRID=4326;POINT (37.61 55.75)",
  "created_at": "2025-12-23T04:36:11.421558+03:00"
}
```

### Поиск точек в радиусе

GET `/api/points/search/`

Query-параметры:
- longitude — долгота
- latitude — широта
- radius — радиус

Пример:
```curl
/api/points/search/?latitude=55.75&longitude=37.61&radius=5
```

### Создание сообщений к точке

POST `/api/points/messages/`

Тело запроса:
```json
{
  "point_id": 1,
  "text": "Отличное место!"
}
```

Ответ:
```json
{
    "id": 1,
    "text": "Отличное место!",
    "author": 1,
    "created_at": "2025-12-23T04:46:30.601172+03:00"
}
```

### Поиск сообщений в радиусе

GET `/api/points/messages/search/`

Query-параметры:
- longitude — долгота
- latitude — широта
- radius — радиус

Пример:
```curl
/api/points/messages/search/?latitude=55.75&longitude=37.61&radius=5
```
Возращает сообщения, связанные с точками, находящимися в заданном радиусе.

---

## Тестирование

В проекте используется `pytest`

Запуск тестов:
```bash
pytest
```
Особенности:
- Тесты моделей и API
- фикстуры через `conftest.py`
- фабрики `make_point`, `make_message`

---

## Архитектурные решения
- GeoDjango + PostGIS используются для гео-фильтрации и расчёта расстояний
- SRID 4326 (WGS84) — стандарт GPS-координат
- BaseCreateView / BaseSearchView — переиспользуемая логика для эндпоинтов
- DRF Serializers — вся валидация входных данных
- Разделение приложений: `points`, `point_messages`

---

## Примечания
- Переопределён BaseUserModel
- Настроенна админ-зона
