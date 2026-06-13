from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.commands.booking_commands import (
    CreateBookingCommand, ExpireBookingCommand, PayBookingCommand
)
from app.application.queries.booking_queries import GetBookingTicketsQuery
from app.presentation.dependencies.dependencies import (
    get_booking_tickets_handler, get_create_booking_handler,
    get_expire_booking_handler, get_pay_booking_handler
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


class CreateBookingRequest(BaseModel):
    event_id: str
    customer_id: str
    ticket_category_id: str
    quantity: int


class PayBookingRequest(BaseModel):
    customer_id: str
    amount: Decimal
    currency: str = "IDR"


@router.post("", status_code=201)
def create_booking(
    body: CreateBookingRequest,
    handler=Depends(get_create_booking_handler)
):
    try:
        booking_id = handler.handle(CreateBookingCommand(
            event_id=body.event_id,
            customer_id=body.customer_id,
            ticket_category_id=body.ticket_category_id,
            quantity=body.quantity,
        ))
        return {"booking_id": booking_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{booking_id}/pay", status_code=200)
def pay_booking(
    booking_id: str,
    body: PayBookingRequest,
    handler=Depends(get_pay_booking_handler)
):
    try:
        handler.handle(PayBookingCommand(
            booking_id=booking_id,
            customer_id=body.customer_id,
            amount=body.amount,
            currency=body.currency,
        ))
        return {"message": "Booking paid successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{booking_id}/expire", status_code=200)
def expire_booking(
    booking_id: str,
    handler=Depends(get_expire_booking_handler)
):
    try:
        handler.handle(ExpireBookingCommand(booking_id=booking_id))
        return {"message": "Booking expired successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{booking_id}")
def get_booking(
    booking_id: str,
    customer_id: str,
    handler=Depends(get_booking_tickets_handler)
):
    try:
        return handler.handle(GetBookingTicketsQuery(
            booking_id=booking_id,
            customer_id=customer_id,
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))