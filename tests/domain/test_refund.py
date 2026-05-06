import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from app.domain.aggregates.booking import Booking, BookingStatus, TicketStatus
from app.domain.aggregates.refund import Refund, RefundStatus
from app.domain.value_objects import BookingId, EventId, Money, TicketCategoryId


def make_paid_booking():
    booking = Booking.create(
        event_id=EventId.generate(),
        customer_id="cust-1",
        ticket_category_id=TicketCategoryId.generate(),
        quantity=1,
        unit_price=Money(Decimal("100000")),
        service_fee=Money(Decimal("0")),
        payment_deadline=datetime.utcnow() + timedelta(minutes=15),
    )
    booking.pay(Money(Decimal("100000")), datetime.utcnow())
    return booking


def test_refund_cannot_be_requested_if_ticket_checked_in():
    from datetime import date
    booking = make_paid_booking()
    ticket = booking.tickets[0]
    event_date = date.today()
    ticket.check_in(event_id=booking.event_id, check_in_date=event_date, event_date=event_date)
    assert booking.has_checked_in_ticket()


def test_refund_can_be_created():
    booking = make_paid_booking()
    refund = Refund.create(booking_id=booking.id, amount=booking.total_price)
    assert refund.status == RefundStatus.REQUESTED


def test_refund_cannot_be_approved_if_not_requested():
    booking = make_paid_booking()
    refund = Refund.create(booking_id=booking.id, amount=booking.total_price)
    refund.approve()
    with pytest.raises(ValueError):
        refund.approve()


def test_refund_rejection_requires_reason():
    booking = make_paid_booking()
    refund = Refund.create(booking_id=booking.id, amount=booking.total_price)
    with pytest.raises(ValueError):
        refund.reject("")


def test_refund_rejected_has_reason():
    booking = make_paid_booking()
    refund = Refund.create(booking_id=booking.id, amount=booking.total_price)
    refund.reject("Policy violation")
    assert refund.status == RefundStatus.REJECTED
    assert refund.rejection_reason == "Policy violation"


def test_refund_paid_out_requires_approved_status():
    booking = make_paid_booking()
    refund = Refund.create(booking_id=booking.id, amount=booking.total_price)
    with pytest.raises(ValueError):
        refund.mark_paid_out("REF-001")


def test_refund_paid_out_records_payment_reference():
    booking = make_paid_booking()
    refund = Refund.create(booking_id=booking.id, amount=booking.total_price)
    refund.approve()
    refund.mark_paid_out("REF-001")
    assert refund.status == RefundStatus.PAID_OUT
    assert refund.payment_reference == "REF-001"