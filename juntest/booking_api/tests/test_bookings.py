from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _future_date():
    from datetime import date, timedelta
    return (date.today() + timedelta(days=1)).isoformat()


def test_create_and_get_booking():
    payload = {
        "name": "Ivan",
        "phone": "+79991234567",
        "booking_date": _future_date(),
        "booking_time": "18:00:00",
        "guests": 4,
    }
    resp = client.post("/bookings", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "active"
    assert body["name"] == "Ivan"

    got = client.get(f"/bookings/{body['id']}")
    assert got.status_code == 200
    assert got.json()["id"] == body["id"]


def test_double_booking_returns_409():
    payload = {
        "name": "Petr",
        "phone": "+79990000000",
        "booking_date": _future_date(),
        "booking_time": "20:00:00",
        "guests": 2,
    }
    assert client.post("/bookings", json=payload).status_code == 201
    second = client.post("/bookings", json=payload)
    assert second.status_code == 409
    assert second.json()["detail"] == "Slot is already booked"


def test_cancel_frees_slot_and_404():
    payload = {
        "name": "Anna",
        "phone": "+79991111111",
        "booking_date": _future_date(),
        "booking_time": "13:00:00",
        "guests": 3,
    }
    created = client.post("/bookings", json=payload).json()
    cancelled = client.delete(f"/bookings/{created['id']}")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"

    # slot is free again
    again = client.post("/bookings", json=payload)
    assert again.status_code == 201

    # unknown id -> 404
    assert client.get("/bookings/999999").status_code == 404