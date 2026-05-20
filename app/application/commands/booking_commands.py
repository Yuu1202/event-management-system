from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateBookingCommand:
    event_id: str
    customer_id: str
    ticket_category_id: str
    quantity: int


@dataclass
class PayBookingCommand:
    booking_id: str
    customer_id: str
    amount: Decimal
    currency: str = "IDR"


@dataclass
class ExpireBookingCommand:
    booking_id: str