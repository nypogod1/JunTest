# Restaurant Booking API

Тестовое задание ОСЬ — Backend Trainee (Python / FastAPI).

REST API для бронирования столика: создать бронь, получить список броней, получить бронь по id и отменить её.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Тесты
python -m pytest -q


Решения

Хранение сделал в памяти (dict), потому что задание  не требует БД. Код разделён на слои: schemas.py (валидация Pydantic v2 — формат телефона, диапазон дат ±30 дней, целые часы 12:00–22:00), service.py (бизнес-логика и проверка занятости слота), routes.py (эндпоинты и статус-коды), main.py (сборка приложения).Ошибки отдаю через HTTPException с сообщениями из ТЗ (Booking not found, Slot is already booked)

Что делал бы дальше:
Подключил бы БД
Больше тестов: границы дат, нецелые часы, неверный формат телефона.
