# Notes API

Небольшое API для работы с заметками на FastAPI.

## Требования

- Python 3.14.3

## Установка

Создать виртуальное окружение:

py -m venv .venv

Активировать виртуальное окружение:

.\.venv\Scripts\Activate.ps1

Установить зависимости в виртуальное окружение:

py -m pip install -r requirements.txt

## Запуск

Запустить приложение:

py -m uvicorn main:app --reload

## Endpoints

GET /health - проверка состояния API.
GET /hello - возвращает приветственное сообщение.
GET /notes - возвращает список заметок.
GET /notes/{note_id} - возвращает заметку по id или 404, если заметка не найдена.
POST /notes - создаёт новую заметку.
HEAD /notes/{note_id} - проверяет существование заметки без возврата тела ответа.
PATCH /notes/{note_id} - частично обновляет существующую заметку.
DELETE /notes/{note_id} - удаляет заметку по id.

## Примеры запросов

**GET /health**

Response:

    {"status": "ok"}

**GET /hello**

Response:

    {"message": "Hello from Notes API"}

**GET /notes**

Response:

    [
      {"id": 1, "title": "Первая заметка", "content": "Текст заметки"}
    ]

**GET /notes/1**

Response:

    {"id": 1, "title": "Первая заметка", "content": "Текст заметки"}

**GET /notes/999**

Response (404):

    {"detail": "Note not found"}


**POST /notes**

Request body:

    {
      "title": "Новая заметка",
      "content": "Текст новой заметки"
    }

Response (201 Created):

    {
      "id": 2,
      "title": "Новая заметка",
      "content": "Текст новой заметки"
    }

**HEAD /notes/1**

Response:

    Status: 200
    Header: x-note-exists: true

**PATCH /notes/1**

Request body:

    {
      "title": "Обновлённая заметка"
    }

Response (200 OK):

    {
      "id": 1,
      "title": "Обновлённая заметка",
      "content": "Текст заметки"
    }

**DELETE /notes/1**

Response:

    Status: 204

    
## Документация

После запуска документация доступна по адресу:

http://127.0.0.1:8000/docs

## Ограничения

Данные хранятся в памяти (`notes = []` в `main.py`) и полностью исчезают при перезапуске приложения.