from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Optional


@dataclass
class CreateEventDTO:
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    max_capacity: int
    organizer_id: str


@dataclass
class CreateTicketCategoryDTO:
    event_id: str
    name: str
    price: Decimal
    quota: int
    sales_start_date: date
    sales_end_date: date


@dataclass
class EventSummaryDTO:
    id: str
    name: str
    start_date: date
    end_date: date
    location: str
    lowest_price: Decimal
    currency: str


@dataclass
class TicketCategoryDTO:
    id: str
    name: str
    price: Decimal
    currency: str
    quota: int
    remaining_quota: int
    sales_start_date: date
    sales_end_date: date
    status: str


@dataclass
class EventDetailDTO:
    id: str
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    organizer_id: str
    status: str
    ticket_categories: List[TicketCategoryDTO]


@dataclass
class SalesReportDTO:
    event_id: str
    total_revenue: Decimal
    currency: str
    total_paid_bookings: int
    total_pending_bookings: int
    total_expired_bookings: int
    total_refunded_bookings: int
    categories: List[dict]


@dataclass
class ParticipantDTO:
    customer_id: str
    ticket_category: str
    ticket_code: str
    check_in_status: str
