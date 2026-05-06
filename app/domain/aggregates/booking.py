from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from app.domain.events import (
    BookingExpired, BookingPaid, DomainEvent, TicketCheckedIn, TicketReserved
)
from app.domain.value_objects import (
    BookingId, EventId, Money, TicketCategoryId, TicketCode, TicketId
)


class BookingStatus(str, Enum):
    PENDING_PAYMENT = "PendingPayment"
    PAID = "Paid"
    EXPIRED = "Expired"
    REFUNDED = "Refunded"


class TicketStatus(str, Enum):
    ACTIVE = "Active"
    CHECKED_IN = "CheckedIn"
    CANCELLED = "Cancelled"
    REFUND_REQUIRED = "RefundRequired"


@dataclass
class Ticket:
    id: TicketId
    booking_id: BookingId
    event_id: EventId
    ticket_code: TicketCode
    status: TicketStatus = TicketStatus.ACTIVE
    _domain_events: List[DomainEvent] = field(default_factory=list, repr=False)

    def check_in(self, event_id: EventId, check_in_date: date, event_date: date):
        if self.event_id != event_id:
            raise ValueError("Ticket does not match the event")
        if self.status == TicketStatus.CHECKED_IN:
            raise ValueError("Ticket has already been checked in")
        if self.status != TicketStatus.ACTIVE:
            raise ValueError("Ticket is not active")
        if check_in_date != event_date:
            raise ValueError("Check-in can only be performed on the event day")
        self.status = TicketStatus.CHECKED_IN
        self._domain_events.append(
            TicketCheckedIn(ticket_id=self.id.value, event_id=event_id.value)
        )

    def cancel(self):
        self.status = TicketStatus.CANCELLED

    def mark_refund_required(self):
        self.status = TicketStatus.REFUND_REQUIRED

    def pull_domain_events(self) -> List[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events


@dataclass
class Booking:
    id: BookingId
    event_id: EventId
    customer_id: str
    ticket_category_id: TicketCategoryId
    quantity: int
    unit_price: Money
    service_fee: Money
    payment_deadline: datetime
    status: BookingStatus = BookingStatus.PENDING_PAYMENT
    tickets: List[Ticket] = field(default_factory=list)
    _domain_events: List[DomainEvent] = field(default_factory=list, repr=False)

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Ticket quantity must be greater than zero")

    @staticmethod
    def create(
        event_id: EventId,
        customer_id: str,
        ticket_category_id: TicketCategoryId,
        quantity: int,
        unit_price: Money,
        service_fee: Money,
        payment_deadline: datetime,
    ) -> "Booking":
        booking_id = BookingId.generate()
        booking = Booking(
            id=booking_id,
            event_id=event_id,
            customer_id=customer_id,
            ticket_category_id=ticket_category_id,
            quantity=quantity,
            unit_price=unit_price,
            service_fee=service_fee,
            payment_deadline=payment_deadline,
        )
        booking._domain_events.append(
            TicketReserved(booking_id=booking_id.value, event_id=event_id.value)
        )
        return booking

    @property
    def total_price(self) -> Money:
        base = self.unit_price.multiply(self.quantity)
        return base.add(self.service_fee)

    def pay(self, amount: Money, paid_at: datetime):
        if self.status != BookingStatus.PENDING_PAYMENT:
            raise ValueError("Booking is not in PendingPayment status")
        if paid_at > self.payment_deadline:
            raise ValueError("Payment deadline has passed")
        if amount != self.total_price:
            raise ValueError("Payment amount does not match total price")
        self.status = BookingStatus.PAID
        self._issue_tickets()
        self._domain_events.append(BookingPaid(booking_id=self.id.value))

    def expire(self):
        if self.status == BookingStatus.PAID:
            raise ValueError("Paid booking cannot be expired")
        if self.status != BookingStatus.PENDING_PAYMENT:
            return
        self.status = BookingStatus.EXPIRED
        self._domain_events.append(BookingExpired(booking_id=self.id.value))

    def mark_refunded(self):
        self.status = BookingStatus.REFUNDED

    def _issue_tickets(self):
        for _ in range(self.quantity):
            ticket = Ticket(
                id=TicketId.generate(),
                booking_id=self.id,
                event_id=self.event_id,
                ticket_code=TicketCode.generate(),
            )
            self.tickets.append(ticket)

    def has_checked_in_ticket(self) -> bool:
        return any(t.status == TicketStatus.CHECKED_IN for t in self.tickets)

    def cancel_tickets(self):
        for ticket in self.tickets:
            ticket.cancel()

    def pull_domain_events(self) -> List[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events