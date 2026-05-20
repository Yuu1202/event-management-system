from datetime import date
from decimal import Decimal
from typing import List

from app.application.commands.event_commands import (
    CancelEventCommand, CreateEventCommand, CreateTicketCategoryCommand,
    DisableTicketCategoryCommand, PublishEventCommand
)
from app.application.dtos.event_dtos import (
    EventDetailDTO, EventSummaryDTO, ParticipantDTO,
    SalesReportDTO, TicketCategoryDTO
)
from app.application.queries.event_queries import (
    GetEventDetailQuery, GetParticipantsQuery,
    GetPublishedEventsQuery, GetSalesReportQuery
)
from app.domain.aggregates.event import Event, EventStatus
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.value_objects import EventId, Money, TicketCategoryId


class CreateEventHandler:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def handle(self, command: CreateEventCommand) -> str:
        event = Event.create(
            name=command.name,
            description=command.description,
            start_date=command.start_date,
            end_date=command.end_date,
            location=command.location,
            max_capacity=command.max_capacity,
            organizer_id=command.organizer_id,
        )
        self._event_repo.save(event)
        return event.id.value


class PublishEventHandler:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def handle(self, command: PublishEventCommand) -> None:
        event = self._event_repo.find_by_id(EventId(command.event_id))
        if event is None:
            raise ValueError("Event not found")
        event.publish()
        self._event_repo.save(event)


class CancelEventHandler:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def handle(self, command: CancelEventCommand) -> None:
        event = self._event_repo.find_by_id(EventId(command.event_id))
        if event is None:
            raise ValueError("Event not found")
        event.cancel()
        self._event_repo.save(event)


class CreateTicketCategoryHandler:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def handle(self, command: CreateTicketCategoryCommand) -> str:
        event = self._event_repo.find_by_id(EventId(command.event_id))
        if event is None:
            raise ValueError("Event not found")
        category = event.add_ticket_category(
            name=command.name,
            price=Money(amount=command.price),
            quota=command.quota,
            sales_start_date=command.sales_start_date,
            sales_end_date=command.sales_end_date,
        )
        self._event_repo.save(event)
        return category.id.value


class DisableTicketCategoryHandler:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def handle(self, command: DisableTicketCategoryCommand) -> None:
        event = self._event_repo.find_by_id(EventId(command.event_id))
        if event is None:
            raise ValueError("Event not found")
        event.disable_ticket_category(TicketCategoryId(command.category_id))
        self._event_repo.save(event)


class GetPublishedEventsHandler:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def handle(self, query: GetPublishedEventsQuery) -> List[EventSummaryDTO]:
        events = self._event_repo.find_all_published()
        result = []
        for event in events:
            active = event.get_active_categories()
            lowest = min((c.price.amount for c in active), default=Decimal("0"))
            currency = active[0].price.currency if active else "IDR"
            if query.location and query.location.lower() not in event.location.lower():
                continue
            result.append(EventSummaryDTO(
                id=event.id.value,
                name=event.name,
                start_date=event.start_date,
                end_date=event.end_date,
                location=event.location,
                lowest_price=lowest,
                currency=currency,
            ))
        return result


class GetEventDetailHandler:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def handle(self, query: GetEventDetailQuery) -> EventDetailDTO:
        event = self._event_repo.find_by_id(EventId(query.event_id))
        if event is None:
            raise ValueError("Event not found")
        today = date.today()
        categories = []
        for c in event.ticket_categories:
            if not c.is_active:
                continue
            if today < c.sales_start_date:
                status = "Coming Soon"
            elif today > c.sales_end_date:
                status = "Sales Closed"
            elif c.remaining_quota == 0:
                status = "Sold Out"
            else:
                status = "Available"
            categories.append(TicketCategoryDTO(
                id=c.id.value,
                name=c.name,
                price=c.price.amount,
                currency=c.price.currency,
                quota=c.quota,
                remaining_quota=c.remaining_quota,
                sales_start_date=c.sales_start_date,
                sales_end_date=c.sales_end_date,
                status=status,
            ))
        return EventDetailDTO(
            id=event.id.value,
            name=event.name,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            organizer_id=event.organizer_id,
            status=event.status.value,
            ticket_categories=categories,
        )


class GetSalesReportHandler:
    def __init__(self, event_repo: EventRepository, booking_repo: BookingRepository):
        self._event_repo = event_repo
        self._booking_repo = booking_repo

    def handle(self, query: GetSalesReportQuery) -> SalesReportDTO:
        from app.domain.aggregates.booking import BookingStatus
        event = self._event_repo.find_by_id(EventId(query.event_id))
        if event is None:
            raise ValueError("Event not found")
        paid = self._booking_repo.find_paid_by_event(EventId(query.event_id))
        total_revenue = sum(b.total_price.amount for b in paid)
        currency = paid[0].total_price.currency if paid else "IDR"
        return SalesReportDTO(
            event_id=query.event_id,
            total_revenue=total_revenue,
            currency=currency,
            total_paid_bookings=len(paid),
            total_pending_bookings=0,
            total_expired_bookings=0,
            total_refunded_bookings=0,
            categories=[],
        )


class GetParticipantsHandler:
    def __init__(self, booking_repo: BookingRepository):
        self._booking_repo = booking_repo

    def handle(self, query: GetParticipantsQuery) -> List[ParticipantDTO]:
        from app.domain.aggregates.booking import TicketStatus
        bookings = self._booking_repo.find_paid_by_event(EventId(query.event_id))
        result = []
        for booking in bookings:
            for ticket in booking.tickets:
                result.append(ParticipantDTO(
                    customer_id=booking.customer_id,
                    ticket_category=booking.ticket_category_id.value,
                    ticket_code=ticket.ticket_code.value,
                    check_in_status=ticket.status.value,
                ))
        return result
