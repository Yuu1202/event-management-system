import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from app.domain.aggregates.booking import Booking, BookingStatus, TicketStatus
from app.domain.value_objects import BookingId, EventId, Money, TicketCategoryId


def make_booking(quantity=2, deadline_offset_minutes=15):
    return Booking.create(
        event_id=EventId.generate(),
        customer_id="cust-1",
        ticket_category_id=TicketCategoryId.generate(),
        quantity=quantity,
        unit_price=Money(Decimal("100000")),
        service_fee=Money(Decimal("0")),
        payment_deadline=datetime.utcnow() + timedelta(minutes=deadline_offset_minutes),
    )


def test_booking_cannot_be_created_with_zero_quantity():
    with pytest.raises(ValueError):
        make_booking(quantity=0)


def test_booking_status_is_pending_payment():
    booking = make_booking()
    assert booking.status == BookingStatus.PENDING_PAYMENT


def test_booking_total_price_is_correct():
    booking = make_booking(quantity=2)
    assert booking.total_price == Money(Decimal("200000"))


def test_booking_can_be_paid():
    booking = make_booking()
    booking.pay(Money(Decimal("200000")), datetime.utcnow())
    assert booking.status == BookingStatus.PAID


def test_booking_cannot_be_paid_after_deadline():
    booking = make_booking(deadline_offset_minutes=-1)
    with pytest.raises(ValueError):
        booking.pay(Money(Decimal("200000")), datetime.utcnow())


def test_booking_cannot_be_paid_with_wrong_amount():
    booking = make_booking()
    with pytest.raises(ValueError):
        booking.pay(Money(Decimal("50000")), datetime.utcnow())


def test_paid_booking_cannot_expire():
    booking = make_booking()
    booking.pay(Money(Decimal("200000")), datetime.utcnow())
    with pytest.raises(ValueError):
        booking.expire()


def test_booking_issues_tickets_after_payment():
    booking = make_booking(quantity=3)
    booking.pay(Money(Decimal("300000")), datetime.utcnow())
    assert len(booking.tickets) == 3


def test_checked_in_ticket_cannot_be_checked_in_again():
    from datetime import date
    booking = make_booking(quantity=1)
    booking.pay(Money(Decimal("100000")), datetime.utcnow())
    ticket = booking.tickets[0]
    event_date = date.today()
    ticket.check_in(event_id=booking.event_id, check_in_date=event_date, event_date=event_date)
    with pytest.raises(ValueError):
        ticket.check_in(event_id=booking.event_id, check_in_date=event_date, event_date=event_date)