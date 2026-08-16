# 💱 Exchange Rate API

**Exchange Rate API** — REST API для получения курсов валют и конвертации денежных сумм между различными валютами.

Приложение построено на **FastAPI** и использует **PostgreSQL** для хранения уже полученных валютных курсов. Если нужного курса нет в базе данных, сервис получает его через внешний **ExchangeRate API**, сохраняет результат и использует его для последующих запросов.

Проект демонстрирует работу с REST API, асинхронным SQLAlchemy, PostgreSQL, Alembic, Docker и внешними API.

---

## ✨ Возможности

- 💱 получение курса между двумя валютами;
- 💰 конвертация указанной суммы из одной валюты в другую;
- 🗄 хранение валют и курсов в PostgreSQL;
- ⚡ использование сохраненного курса без повторного запроса к внешнему API;
- 🌐 автоматическое получение отсутствующего курса через ExchangeRate API;
- 📚 интерактивная Swagger-документация;
- 🐳 запуск приложения и PostgreSQL через Docker Compose;
- 🔄 управление схемой базы данных через Alembic.

---

## 🛠 Стек технологий

| Технология | Назначение |
|---|---|
| Python | Основной язык проекта |
| FastAPI | REST API framework |
| Uvicorn | ASGI-сервер |
| Gunicorn | Запуск приложения в production-среде |
| PostgreSQL | Хранение валют и курсов |
| SQLAlchemy 2 | ORM и работа с базой данных |
| asyncpg | Асинхронный PostgreSQL-драйвер |
| psycopg / psycopg2 | PostgreSQL-драйверы |
| Alembic | Миграции базы данных |
| Requests | Запросы к внешнему ExchangeRate API |
| python-dotenv | Загрузка переменных окружения |
| Loguru | Логирование |
| Docker | Контейнеризация приложения |
| Docker Compose | Запуск API и PostgreSQL |

---

## 📁 Структура проекта

```text
exchange_rate/
├── app/
│   ├── db/
│   │   ├── models/           # SQLAlchemy-модели
│   │   ├── config.py         # Подключение к PostgreSQL
│   │   ├── queries.py        # Запросы к базе данных
│   │   └── __init__.py
│   │
│   ├── handlers.py           # FastAPI endpoints
│   ├── services.py           # Работа с ExchangeRate API
│   └── __init__.py
│
├── migrations/               # Alembic migrations
├── main.py                   # Точка входа FastAPI
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── Makefile
├── requirements.txt
└── .gitignore
```

---

## 🔄 Как работает приложение

Логика получения курса выглядит следующим образом:

```text
Client
  │
  ▼
FastAPI endpoint
  │
  ▼
Проверка PostgreSQL
  │
  ├── Курс найден ─────────────► Возврат результата
  │
  └── Курс не найден
          │
          ▼
    ExchangeRate API
          │
          ▼
    Сохранение курса в БД
          │
          ▼
    Возврат результата
```

Таким образом, приложение сначала пытается использовать данные из собственной базы.

Если валютная пара отсутствует, сервис делает запрос к внешнему API, сохраняет валюты и полученный курс в PostgreSQL, после чего возвращает результат пользователю.

---

## 🌐 API

После запуска приложения Swagger UI доступен по адресу:

```text
http://localhost:8000/
```

В проекте корневая страница `/` используется непосредственно для Swagger-документации.

---

## 📊 Получение курса валют

### Endpoint

```http
GET /conversion_rate/{base}/{target}
```

### Пример

Получить курс доллара США к евро:

```http
GET /conversion_rate/USD/EUR
```

Пример через `curl`:

```bash
curl http://localhost:8000/conversion_rate/USD/EUR
```

Параметры:

| Параметр | Описание |
|---|---|
| `base` | Исходная валюта |
| `target` | Валюта назначения |

В качестве кодов валют используются стандартные обозначения:

```text
USD
EUR
GBP
AMD
RUB
JPY
и т.д.
```

---

## 💰 Конвертация валют

### Endpoint

```http
GET /conversion/{base}/{target}/{amount}
```

### Пример

Конвертировать `100 USD` в `EUR`:

```http
GET /conversion/USD/EUR/100
```

Через `curl`:

```bash
curl http://localhost:8000/conversion/USD/EUR/100
```

Параметры:

| Параметр | Описание |
|---|---|
| `base` | Исходная валюта |
| `target` | Валюта назначения |
| `amount` | Сумма для конвертации |

---

## 🚀 Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/SergoAr3/exchange_rate.git
cd exchange_rate
```

---

## 🔐 Переменные окружения

Создайте `.env` в корне проекта.

Пример:

```env
EXCHANGE_API_KEY=your_exchange_rate_api_key

DATABASE_URL=postgresql+asyncpg://postgres:sergo@db:5432/exchange_rates
```

### `EXCHANGE_API_KEY`

API-ключ используется для получения актуальных валютных курсов через внешний ExchangeRate API.

### `DATABASE_URL`

Строка подключения SQLAlchemy к PostgreSQL.

Для Docker Compose:

```env
DATABASE_URL=postgresql+asyncpg://postgres:sergo@db:5432/exchange_rates
```

Для локально запущенного PostgreSQL:

```env
DATABASE_URL=postgresql+asyncpg://postgres:sergo@localhost:5432/exchange_rates
```

> Не добавляйте `.env` и API-ключи в GitHub.

---

## 🐳 Запуск через Docker

Для запуска приложения вместе с PostgreSQL:

```bash
docker compose up --build
```

После запуска API будет доступен по адресу:

```text
http://localhost:8000/
```

В Docker Compose запускаются два сервиса:

```text
db
└── PostgreSQL

app
└── FastAPI application
```

Для запуска контейнеров в фоновом режиме:

```bash
docker compose up -d --build
```

Просмотр логов:

```bash
docker compose logs -f
```

Остановка:

```bash
docker compose down
```

---

## 💻 Локальный запуск

### 1. Создание виртуального окружения

```bash
python -m venv venv
```

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

### 3. Настройка `.env`

Для локального запуска PostgreSQL:

```env
EXCHANGE_API_KEY=your_exchange_rate_api_key

DATABASE_URL=postgresql+asyncpg://postgres:sergo@localhost:5432/exchange_rates
```

---

### 4. Применение миграций

```bash
alembic upgrade head
```

или:

```bash
make migrate
```

---

### 5. Запуск FastAPI

```bash
python main.py
```

После запуска:

```text
http://localhost:8000/
```

---

## 🗄 База данных

Проект использует PostgreSQL.

Подключение создается через асинхронный SQLAlchemy engine:

```text
FastAPI
   │
   ▼
SQLAlchemy AsyncSession
   │
   ▼
asyncpg
   │
   ▼
PostgreSQL
```

В базе сохраняются:

- валюты;
- валютные пары;
- полученные курсы обмена.

Это позволяет повторно использовать уже полученный курс без запроса к внешнему API.

---

## 🔄 Миграции

Для управления схемой базы данных используется **Alembic**.

Применить существующие миграции:

```bash
alembic upgrade head
```

или:

```bash
make migrate
```

Создать новую миграцию:

```bash
make migration NAME="migration_name"
```

---

## ▶️ Точка входа

Основное FastAPI-приложение находится в `main.py`.

```python
app = FastAPI(docs_url="/")
```

После этого подключается router с endpoint-ами валютного сервиса:

```python
app.include_router(router, tags=["currencies"])
```

При непосредственном запуске используется Uvicorn:

```bash
python main.py
```

---

## 🔌 Работа с внешним API

Если валютный курс отсутствует в PostgreSQL, приложение формирует запрос вида:

```text
/v6/{API_KEY}/pair/{base}/{target}
```

После получения ответа:

1. извлекается `conversion_rate`;
2. исходная валюта сохраняется в базе;
3. целевая валюта сохраняется в базе;
4. валютный курс сохраняется в PostgreSQL;
5. результат возвращается клиенту.

При последующих запросах приложение может получить курс непосредственно из базы данных.

---

## 📦 Основные зависимости

Основные библиотеки проекта:

```text
FastAPI
SQLAlchemy
asyncpg
Alembic
Requests
Uvicorn
Gunicorn
python-dotenv
Loguru
```

Полный список расположен в:

```text
requirements.txt
```

---

## 📌 Что можно улучшить

Возможные направления дальнейшего развития проекта:

- добавить срок жизни сохраненных валютных курсов;
- автоматически обновлять устаревшие курсы;
- заменить синхронный `requests` на асинхронный HTTP-клиент;
- добавить Redis-кеширование;
- добавить Pydantic response models;
- реализовать централизованную обработку ошибок внешнего API;
- добавить валидацию кодов валют;
- добавить unit- и integration-тесты;
- настроить GitHub Actions;
- добавить health-check endpoint;
- скрыть данные PostgreSQL из `docker-compose.yml` в переменные окружения;
- добавить production-конфигурацию Gunicorn/Uvicorn.

---

## ⚠️ Важно

Проект использует данные внешнего ExchangeRate API.

Для работы приложения необходим действующий API-ключ:

```env
EXCHANGE_API_KEY=...
```

Доступность и актуальность валютных курсов зависят от используемого внешнего сервиса.
