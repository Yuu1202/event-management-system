from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class CreateEventCommand:
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    max_capacity: int
    organizer_id: str


@dataclass
class PublishEventCommand:
    event_id: str
    organizer_id: str


@dataclass
class CancelEventCommand:
    event_id: str
    organizer_id: str


@dataclass
class CreateTicketCategoryCommand:
    event_id: str
    name: str
    price: Decimal
    quota: int
    sales_start_date: date
    sales_end_date: date
    organizer_id: str


@dataclass
class DisableTicketCategoryCommand:
    event_id: str
    category_id: str
    organizer_id: str
