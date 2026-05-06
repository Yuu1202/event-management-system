import pytest
from datetime import date
from decimal import Decimal

from app.domain.aggregates.event import Event, EventStatus
from app.domain.value_objects import EventId, Money


def make_event(**kwargs):
    defaults = dict(
        name="Test Event",
        description="Desc",
        start_date=date(2025, 12, 1),
        end_date=date(2025, 12, 2),
        location="Surabaya",
        max_capacity=100,
        organizer_id="org-1",
    )
    defaults.update(kwargs)
    return Event.create(**defaults)


def add_category(event, quota=50):
    return event.add_ticket_category(
        name="Regular",
        price=Money(Decimal("100000")),
        quota=quota,
        sales_start_date=date(2025, 11, 1),
        sales_end_date=date(2025, 11, 30),
    )


def test_event_cannot_be_created_with_invalid_schedule():
    with pytest.raises(ValueError):
        make_event(start_date=date(2025, 12, 5), end_date=date(2025, 12, 1))


def test_event_cannot_be_created_with_zero_capacity():
    with pytest.raises(ValueError):
        make_event(max_capacity=0)


def test_event_cannot_be_created_with_negative_capacity():
    with pytest.raises(ValueError):
        make_event(max_capacity=-1)


def test_event_created_status_is_draft():
    event = make_event()
    assert event.status == EventStatus.DRAFT


def test_event_raises_event_created_domain_event():
    event = make_event()
    events = event.pull_domain_events()
    assert any(e._class.name_ == "EventCreated" for e in events)


def test_event_cannot_be_published_without_active_category():
    event = make_event()
    with pytest.raises(ValueError):
        event.publish()


def test_event_can_be_published_with_active_category():
    event = make_event()
    add_category(event)
    event.publish()
    assert event.status == EventStatus.PUBLISHED


def test_ticket_category_quota_cannot_exceed_event_capacity():
    event = make_event(max_capacity=50)
    with pytest.raises(ValueError):
        add_category(event, quota=100)


def test_cancelled_event_cannot_be_published():
    event = make_event()
    add_category(event)
    event.publish()
    event.cancel()
    with pytest.raises(ValueError):
        event.publish()