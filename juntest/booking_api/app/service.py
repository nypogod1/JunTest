from datetime import date
from typing import Optional

from fastapi import HTTPException

from .schemas import BookingCreate, BookingOut


class BookingService:
    
    def __init__(self) -> None:
        self._store: dict[int, dict] = {}
        self._next_id: int = 1

    def create(self, data: BookingCreate) -> BookingOut:
        if self._slot_taken(data.booking_date, data.booking_time):
            raise HTTPException(status_code=409, detail="Slot is already booked")

        booking_id = self._next_id
        self._next_id += 1

        record = {
            "id": booking_id,
            "name": data.name,
            "phone": data.phone,
            "booking_date": data.booking_date,
            "booking_time": data.booking_time,
            "guests": data.guests,
            "status": "active",
        }
        self._store[booking_id] = record
        return BookingOut(**record)

    def list(self, booking_date: Optional[date] = None) -> list[BookingOut]:
        records = self._store.values()
        if booking_date is not None:
            records = [r for r in records if r["booking_date"] == booking_date]
        return [BookingOut(**r) for r in records]

    def get(self, booking_id: int) -> BookingOut:
        record = self._store.get(booking_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        return BookingOut(**record)

    def cancel(self, booking_id: int) -> BookingOut:
        record = self._store.get(booking_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        record["status"] = "cancelled"
        return BookingOut(**record)

    def _slot_taken(self, booking_date: date, booking_time) -> bool:
        return any(
            r["booking_date"] == booking_date
            and r["booking_time"] == booking_time
            and r["status"] == "active"
            for r in self._store.values()
        )

booking_service = BookingService()