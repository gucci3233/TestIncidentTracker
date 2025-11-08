Incident Tracker API
---

## Технологии

* **Python 3.12**
* **FastAPI**
* **PostgreSQL 15**
* **Docker & Docker Compose**
* **Uvicorn** (ASGI сервер)


## Запуск через Docker

### 1. Сборка и запуск с Docker Compose

* используем .env.copy
```bash
docker compose --env-file .env.copy up --build -d 
```

### 3. Проверка через Docker

```bash
docker-compose ps
docker-compose logs web
```

---

## Документация API

Если `DEBUG=True`:

* Swagger UI: [http://localhost:8005/docs/](http://localhost:8005/docs/)
* Redoc: [http://localhost:8005/redoc/](http://localhost:8005/redoc/)

### Эндпоинты API

Основной роутер находится в `sources/api/v1/routers/incident.py`. Пример:

| Endpoint                  | Method | Назначение                        |
| ------------------------- | ------ | --------------------------------- |
| `/api/v1/incidents/`      | GET    | Получение списка инцидентов       |
| `/api/v1/incidents/`      | POST   | Добавление нового инцидента       |
| `/api/v1/incidents/{id}/` | GET    | Получение деталей инцидента       |
| `/api/v1/incidents/{id}/` | PUT    | Обновление информации о инциденте |
| `/api/v1/incidents/{id}/` | DELETE | Удаление инцидента                |


---


> Эндпоинты будут доступны по адресу `http://localhost:8005/docs/`.

---

## Полезные команды

* **Остановка контейнеров Docker**:

```bash
docker-compose down
```

* **Подключение к базе данных**:

```bash
docker exec -it <db_container_name> psql -U main_user -d incident_db
```

* **Просмотр логов**:

```bash
docker-compose logs -f web
```

---

## Структура проекта

```
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── main.py
├── readme.md
├── requirements.txt
└── sources
    ├── api
    │   ├── __init__.py
    │   └── v1
    │       ├── __init__.py
    │       ├── routers
    │       │   ├── incident.py
    │       │   └── __init__.py
    │       └── schemas
    │           ├── incident.py
    │           └── __init__.py
    ├── core
    │   ├── config.py
    │   └── __init__.py
    ├── database
    │   ├── base.py
    │   ├── __init__.py
    │   └── mixins
    │       ├── __init__.py
    │       └── manager.py
    ├── __init__.py
    └── models
        ├── incident.py
        └── __init__.py

```

* `main.py` – запускает FastAPI сервер
* `sources/` – роутеры API, схемы, CRUD, сервисы
* `alembic/` – миграции базы данных

---
