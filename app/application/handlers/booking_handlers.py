from datetime import datetime
from decimal import Decimal

from app.application.commands.booking_commands import (
    CreateBookingCommand, ExpireBookingCommand, PayBookingCommand
)
from app.application.dtos.booking_dtos import BookingDetailDTO, TicketDTO
from app.application.interfaces.notification_service import NotificationServiceInterface
from app.application.interfaces.payment_gateway import PaymentGatewayInterface
from app.application.queries.booking_queries import GetBookingTicketsQuery
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.services.booking_service import BookingService
from app.domain.value_objects import BookingId, EventId, Money, TicketCategoryId


class CreateBookingHandler:
    def __init__(self, event_repo: EventRepository, booking_repo: BookingRepository):
        self._event_repo = event_repo
        self._booking_repo = booking_repo
        self._service = BookingService()

    def handle(self, command: CreateBookingCommand) -> str:
        event = self._event_repo.find_by_id(EventId(command.event_id))
        if event is None:
            raise ValueError("Event not found")
        existing = self._booking_repo.find_by_customer_and_event(
            command.customer_id, EventId(command.event_id)
        )
        booking = self._service.create_booking(
            event=event,
            customer_id=command.customer_id,
            category_id=TicketCategoryId(command.ticket_category_id),
            quantity=command.quantity,
            existing_booking=existing,
        )
        self._booking_repo.save(booking)
        self._event_repo.save(event)
        return booking.id.value


class PayBookingHandler:
    def __init__(
        self,
        booking_repo: BookingRepository,
        payment_gateway: PaymentGatewayInterface,
        notification_service: NotificationServiceInterface,
    ):
        self._booking_repo = booking_repo
        self._payment_gateway = payment_gateway
        self._notification_service = notification_service

    def handle(self, command: PayBookingCommand) -> None:
        booking = self._booking_repo.find_by_id(BookingId(command.booking_id))
        if booking is None:
            raise ValueError("Booking not found")
        amount = Money(amount=command.amount, currency=command.currency)
        self._payment_gateway.process_payment(command.booking_id, command.amount, command.currency)
        booking.pay(amount, datetime.utcnow())
        self._booking_repo.save(booking)
        self._notification_service.send_payment_confirmation(command.customer_id, command.booking_id)


class ExpireBookingHandler:
    def __init__(self, booking_repo: BookingRepository, event_repo: EventRepository):
        self._booking_repo = booking_repo
        self._event_repo = event_repo

    def handle(self, command: ExpireBookingCommand) -> None:
        booking = self._booking_repo.find_by_id(BookingId(command.booking_id))
        if booking is None:
            raise ValueError("Booking not found")
        event = self._event_repo.find_by_id(booking.event_id)
        booking.expire()
        if event:
            for c in event.ticket_categories:
                if c.id == booking.ticket_category_id:
                    c.release(booking.quantity)
            self._event_repo.save(event)
        self._booking_repo.save(booking)


class GetBookingTicketsHandler:
    def __init__(self, booking_repo: BookingRepository):
        self._booking_repo = booking_repo

    def handle(self, query: GetBookingTicketsQuery) -> BookingDetailDTO:
        booking = self._booking_repo.find_by_id(BookingId(query.booking_id))
        if booking is None:
            raise ValueError("Booking not found")
        tickets = [
            TicketDTO(id=t.id.value, ticket_code=t.ticket_code.value, status=t.status.value)
            for t in booking.tickets
        ]
        return BookingDetailDTO(
            id=booking.id.value,
            event_id=booking.event_id.value,
            customer_id=booking.customer_id,
            ticket_category_id=booking.ticket_category_id.value,
            quantity=booking.quantity,
            total_price=booking.total_price.amount,
            currency=booking.total_price.currency,
            status=booking.status.value,
            payment_deadline=booking.payment_deadline,
            tickets=tickets,
        )