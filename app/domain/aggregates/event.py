from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional

from app.domain.events import (
    DomainEvent, EventCancelled, EventCreated, EventPublished,
    TicketCategoryCreated, TicketCategoryDisabled
)
from app.domain.value_objects import EventId, Money, TicketCategoryId


class EventStatus(str, Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class TicketCategoryStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


@dataclass
class TicketCategory:
    id: TicketCategoryId
    event_id: EventId
    name: str
    price: Money
    quota: int
    sales_start_date: date
    sales_end_date: date
    status: TicketCategoryStatus = TicketCategoryStatus.ACTIVE
    booked_count: int = 0

    @property
    def remaining_quota(self) -> int:
        return self.quota - self.booked_count

    @property
    def is_active(self) -> bool:
        return self.status == TicketCategoryStatus.ACTIVE

    def disable(self):
        self.status = TicketCategoryStatus.INACTIVE

    def reserve(self, quantity: int):
        if self.remaining_quota < quantity:
            raise ValueError("Not enough quota")
        self.booked_count += quantity

    def release(self, quantity: int):
        self.booked_count = max(0, self.booked_count - quantity)


@dataclass
class Event:
    id: EventId
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    max_capacity: int
    organizer_id: str
    status: EventStatus = EventStatus.DRAFT
    ticket_categories: List[TicketCategory] = field(default_factory=list)
    _domain_events: List[DomainEvent] = field(default_factory=list, repr=False)

    def __post_init__(self):  # FIX: Gunakan double underscore
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date")
        if self.max_capacity <= 0:
            raise ValueError("Max capacity must be greater than zero")

    @staticmethod
    def create(
        name: str,
        description: str,
        start_date: date,
        end_date: date,
        location: str,
        max_capacity: int,
        organizer_id: str,
    ) -> "Event":
    
        # Validasi manual di sini agar fail-fast
        if end_date < start_date:
            raise ValueError("End date cannot be earlier than start date")
        if max_capacity <= 0:
            raise ValueError("Max capacity must be greater than zero")

        event_id = EventId.generate()
        event = Event(
            id=event_id,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            location=location,
            max_capacity=max_capacity,
            organizer_id=organizer_id,
        )
        event._domain_events.append(EventCreated(event_id=event_id.value, name=name))
        return event
    

    def publish(self):
        if self.status == EventStatus.CANCELLED:
            raise ValueError("Cancelled event cannot be published")
        active_categories = [c for c in self.ticket_categories if c.is_active]
        if not active_categories:
            raise ValueError("Event must have at least one active ticket category")
        total_quota = sum(c.quota for c in active_categories)
        if total_quota > self.max_capacity:
            raise ValueError("Total ticket quota exceeds max capacity")
        self.status = EventStatus.PUBLISHED
        self._domain_events.append(EventPublished(event_id=self.id.value))

    def cancel(self):
        if self.status == EventStatus.COMPLETED:
            raise ValueError("Completed event cannot be cancelled")
        self.status = EventStatus.CANCELLED
        self._domain_events.append(EventCancelled(event_id=self.id.value))

    def add_ticket_category(
        self,
        name: str,
        price: Money,
        quota: int,
        sales_start_date: date,
        sales_end_date: date,
    ) -> TicketCategory:
        if price.amount < 0:
            raise ValueError("Ticket price cannot be negative")
        if quota <= 0:
            raise ValueError("Ticket quota must be greater than zero")
        if sales_end_date > self.start_date:
            raise ValueError("Sales period must end before or at event start date")
        total_quota = sum(c.quota for c in self.ticket_categories) + quota
        if total_quota > self.max_capacity:
            raise ValueError("Total quota exceeds max event capacity")

        category_id = TicketCategoryId.generate()
        category = TicketCategory(
            id=category_id,
            event_id=self.id,
            name=name,
            price=price,
            quota=quota,
            sales_start_date=sales_start_date,
            sales_end_date=sales_end_date,
        )
        self.ticket_categories.append(category)
        self._domain_events.append(
            TicketCategoryCreated(event_id=self.id.value, category_id=category_id.value)
        )
        return category

    def disable_ticket_category(self, category_id: TicketCategoryId):
        category = self._get_category(category_id)
        if self.status == EventStatus.COMPLETED:
            raise ValueError("Cannot disable category of a completed event")
        category.disable()
        self._domain_events.append(
            TicketCategoryDisabled(event_id=self.id.value, category_id=category_id.value)
        )

    def _get_category(self, category_id: TicketCategoryId) -> TicketCategory:
        for c in self.ticket_categories:
            if c.id == category_id:
                return c
        raise ValueError("Ticket category not found")

    def get_active_categories(self) -> List[TicketCategory]:
        return [c for c in self.ticket_categories if c.is_active]

    def pull_domain_events(self) -> List[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events