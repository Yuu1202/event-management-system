from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.aggregates.booking import Booking, BookingStatus, Ticket, TicketStatus
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.value_objects import BookingId, EventId, Money, TicketCategoryId, TicketCode, TicketId
from app.infrastructure.database.models import BookingModel, TicketModel


class SQLAlchemyBookingRepository(BookingRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, booking: Booking) -> None:
        model = self._session.get(BookingModel, booking.id.value)
        if model is None:
            model = BookingModel(id=booking.id.value)
            self._session.add(model)

        model.event_id = booking.event_id.value
        model.customer_id = booking.customer_id
        model.ticket_category_id = booking.ticket_category_id.value
        model.quantity = booking.quantity
        model.unit_price_amount = booking.unit_price.amount
        model.unit_price_currency = booking.unit_price.currency
        model.service_fee_amount = booking.service_fee.amount
        model.service_fee_currency = booking.service_fee.currency
        model.payment_deadline = booking.payment_deadline
        model.status = booking.status.value

        existing_ids = {t.id for t in model.tickets}
        for ticket in booking.tickets:
            if ticket.id.value not in existing_ids:
                ticket_model = TicketModel(
                    id=ticket.id.value,
                    booking_id=booking.id.value,
                    event_id=ticket.event_id.value,
                    ticket_code=ticket.ticket_code.value,
                    status=ticket.status.value,
                )
                model.tickets.append(ticket_model)
            else:
                t_model = next(t for t in model.tickets if t.id == ticket.id.value)
                t_model.status = ticket.status.value

        self._session.commit()

    def find_by_id(self, booking_id: BookingId) -> Optional[Booking]:
        model = self._session.get(BookingModel, booking_id.value)
        if model is None:
            return None
        return self._to_domain(model)

    def find_by_customer_and_event(self, customer_id: str, event_id: EventId) -> Optional[Booking]:
        model = self._session.query(BookingModel).filter(
            BookingModel.customer_id == customer_id,
            BookingModel.event_id == event_id.value,
            BookingModel.status.in_(["PendingPayment", "Paid"]),
        ).first()
        return self._to_domain(model) if model else None

    def find_paid_by_event(self, event_id: EventId) -> List[Booking]:
        models = self._session.query(BookingModel).filter(
            BookingModel.event_id == event_id.value,
            BookingModel.status == BookingStatus.PAID.value,
        ).all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: BookingModel) -> Booking:
        booking = Booking(
            id=BookingId(model.id),
            event_id=EventId(model.event_id),
            customer_id=model.customer_id,
            ticket_category_id=TicketCategoryId(model.ticket_category_id),
            quantity=model.quantity,
            unit_price=Money(amount=model.unit_price_amount, currency=model.unit_price_currency),
            service_fee=Money(amount=model.service_fee_amount, currency=model.service_fee_currency),
            payment_deadline=model.payment_deadline,
            status=BookingStatus(model.status),
        )
        for t in model.tickets:
            ticket = Ticket(
                id=TicketId(t.id),
                booking_id=BookingId(t.booking_id),
                event_id=EventId(t.event_id),
                ticket_code=TicketCode(t.ticket_code),
                status=TicketStatus(t.status),
            )
            booking.tickets.append(ticket)
        return booking
