from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass
class CreateBookingDTO:
    event_id: str
    customer_id: str
    ticket_category_id: str
    quantity: int


@dataclass
class PayBookingDTO:
    booking_id: str
    amount: Decimal
    currency: str = "IDR"


@dataclass
class TicketDTO:
    id: str
    ticket_code: str
    status: str


@dataclass
class BookingDetailDTO:
    id: str
    event_id: str
    customer_id: str
    ticket_category_id: str
    quantity: int
    total_price: Decimal
    currency: str
    status: str
    payment_deadline: datetime
    tickets: List[TicketDTO]