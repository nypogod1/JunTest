from datetime import date
from typing import Optional

from fastapi import APIRouter, Query, status

from .schemas import BookingCreate, BookingOut
from .service import booking_service

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate) -> BookingOut:
    return booking_service.create(payload)


@router.get("", response_model=list[BookingOut])
def list_bookings(
    date_filter: Optional[date] = Query(default=None, alias="date"),
) -> list[BookingOut]:
    return booking_service.list(date_filter)


@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int) -> BookingOut:
    return booking_service.get(booking_id)


@router.delete("/{booking_id}", response_model=BookingOut)
def cancel_booking(booking_id: int) -> BookingOut:
    return booking_service.cancel(booking_id)