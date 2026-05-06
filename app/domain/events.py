from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DomainEvent:
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EventCreated(DomainEvent):
    event_id: str = ""
    name: str = ""


@dataclass
class EventPublished(DomainEvent):
    event_id: str = ""


@dataclass
class EventCancelled(DomainEvent):
    event_id: str = ""


@dataclass
class TicketCategoryCreated(DomainEvent):
    event_id: str = ""
    category_id: str = ""


@dataclass
class TicketCategoryDisabled(DomainEvent):
    event_id: str = ""
    category_id: str = ""


@dataclass
class TicketReserved(DomainEvent):
    booking_id: str = ""
    event_id: str = ""


@dataclass
class BookingPaid(DomainEvent):
    booking_id: str = ""


@dataclass
class BookingExpired(DomainEvent):
    booking_id: str = ""


@dataclass
class TicketCheckedIn(DomainEvent):
    ticket_id: str = ""
    event_id: str = ""


@dataclass
class RefundRequested(DomainEvent):
    refund_id: str = ""
    booking_id: str = ""


@dataclass
class RefundApproved(DomainEvent):
    refund_id: str = ""


@dataclass
class RefundRejected(DomainEvent):
    refund_id: str = ""
    reason: str = ""


@dataclass
class RefundPaidOut(DomainEvent):
    refund_id: str = ""
    payment_reference: str = ""