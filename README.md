# Notes API

Небольшое API для работы с заметками на FastAPI.

## Установка

Установить зависимости:

py -m pip install -r requirements.txt

## Запуск

Запустить приложение:

py -m uvicorn main:app --reload

## Endpoints

GET /health - проверка состояния API.
GET /hello - возвращает приветственное сообщение.
GET /notes - возвращает список заметок.
POST /notes - создаёт новую заметку.

## Документация

После запуска документация доступна по адресу:

http://127.0.0.1:8000/docs