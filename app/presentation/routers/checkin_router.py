from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.domain.repositories.booking_repository import BookingRepository
from app.domain.value_objects import EventId, TicketCode
from app.presentation.dependencies.dependencies import get_booking_repo

router = APIRouter(prefix="/checkin", tags=["Check-in"])


class CheckInRequest(BaseModel):
    ticket_code: str
    event_id: str


@router.post("", status_code=200)
def check_in_ticket(
    body: CheckInRequest,
    booking_repo: BookingRepository = Depends(get_booking_repo)
):
    try:
        bookings = booking_repo.find_paid_by_event(EventId(body.event_id))
        ticket = None
        booking = None
        for b in bookings:
            for t in b.tickets:
                if t.ticket_code.value == body.ticket_code:
                    ticket = t
                    booking = b
                    break
            if ticket:
                break

        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket is invalid")

        today = date.today()
        ticket.check_in(
            event_id=EventId(body.event_id),
            check_in_date=today,
            event_date=today,
        )
        booking_repo.save(booking)
        return {"message": "Check-in successful", "ticket_code": body.ticket_code}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))