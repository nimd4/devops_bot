# Docker

## Описание

Данная ветка проект представляет собой Telegram-бота на Python с использованием PostgreSQL.

Проект предназначен для развертывания при помощи Docker и Docker Compose.

## Структура проекта

```
devops_bot/
│
├── bot/
│   ├── bot.py
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── db/
│   ├── init.sql
│   └── Dockerfile
│
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

## Используемые технологии

- Python 3
- python-telegram-bot
- PostgreSQL
- psycopg2
- Docker
- Docker Compose

## Предварительные требования

Перед запуском должны быть установлены:

- Docker
- Docker Compose

Проверка установки:

```bash
docker --version
docker compose version
```

## Настройка

Создайте файл `.env` в корневой директории проекта.

Пример содержимого:

```env
BOT_TOKEN=bot_token

DB_HOST=db
DB_PORT=5432
DB_NAME=tg_bot_db
DB_USER=bot_user
DB_PASSWORD=bot_password
```

## Сборка проекта

Из корня проекта выполните:

```bash
docker compose build
```

## Запуск проекта

```bash
docker compose up -d
```

Проверить состояние контейнеров:

```bash
docker compose ps
```

Просмотреть логи:

```bash
docker compose logs
```

Логи Telegram-бота:

```bash
docker compose logs bot
```

Логи PostgreSQL:

```bash
docker compose logs db
```

## Остановка проекта

```bash
docker compose down
```

## Проверка работы

После запуска:

1. Убедиться, что контейнеры находятся в состоянии `Up`:

```bash
docker compose ps
```

2. Открыть Telegram.

3. Найти своего бота.

4. Выполнить команду:

```
/start
```

После этого бот должен вывести меню с доступными действиями.
