from datetime import datetime, timedelta

from app.domain.aggregates.booking import Booking
from app.domain.aggregates.event import Event, EventStatus, TicketCategory
from app.domain.value_objects import BookingId, EventId, Money, TicketCategoryId


class BookingService:

    PAYMENT_DEADLINE_MINUTES = 15

    def create_booking(
        self,
        event: Event,
        customer_id: str,
        category_id: TicketCategoryId,
        quantity: int,
        existing_booking: Booking = None,
    ) -> Booking:
        if event.status != EventStatus.PUBLISHED:
            raise ValueError("Booking can only be created for a published event")

        category = self._get_active_category(event, category_id)
        today = datetime.utcnow().date()

        if today < category.sales_start_date or today > category.sales_end_date:
            raise ValueError("Booking is outside the ticket sales period")

        if existing_booking is not None:
            raise ValueError("Customer already has an active booking for this event")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if category.remaining_quota < quantity:
            raise ValueError("Not enough remaining quota")

        service_fee = Money(amount=0)
        payment_deadline = datetime.utcnow() + timedelta(minutes=self.PAYMENT_DEADLINE_MINUTES)

        booking = Booking.create(
            event_id=event.id,
            customer_id=customer_id,
            ticket_category_id=category_id,
            quantity=quantity,
            unit_price=category.price,
            service_fee=service_fee,
            payment_deadline=payment_deadline,
        )

        category.reserve(quantity)
        return booking

    def _get_active_category(self, event: Event, category_id: TicketCategoryId) -> TicketCategory:
        for c in event.ticket_categories:
            if c.id == category_id and c.is_active:
                return c
        raise ValueError("Ticket category not found or inactive")