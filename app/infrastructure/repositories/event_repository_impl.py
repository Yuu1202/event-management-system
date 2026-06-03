from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.aggregates.event import Event, EventStatus, TicketCategory, TicketCategoryStatus
from app.domain.repositories.event_repository import EventRepository
from app.domain.value_objects import EventId, Money, TicketCategoryId
from app.infrastructure.database.models import EventModel, TicketCategoryModel


class SQLAlchemyEventRepository(EventRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, event: Event) -> None:
        model = self._session.get(EventModel, event.id.value)
        if model is None:
            model = EventModel(id=event.id.value)
            self._session.add(model)

        model.name = event.name
        model.description = event.description
        model.start_date = event.start_date
        model.end_date = event.end_date
        model.location = event.location
        model.max_capacity = event.max_capacity
        model.organizer_id = event.organizer_id
        model.status = event.status.value

        existing_ids = {m.id for m in model.ticket_categories}
        for category in event.ticket_categories:
            if category.id.value in existing_ids:
                cat_model = next(m for m in model.ticket_categories if m.id == category.id.value)
            else:
                cat_model = TicketCategoryModel(id=category.id.value, event_id=event.id.value)
                model.ticket_categories.append(cat_model)

            cat_model.name = category.name
            cat_model.price_amount = category.price.amount
            cat_model.price_currency = category.price.currency
            cat_model.quota = category.quota
            cat_model.booked_count = category.booked_count
            cat_model.sales_start_date = category.sales_start_date
            cat_model.sales_end_date = category.sales_end_date
            cat_model.status = category.status.value

        self._session.commit()

    def find_by_id(self, event_id: EventId) -> Optional[Event]:
        model = self._session.get(EventModel, event_id.value)
        if model is None:
            return None
        return self._to_domain(model)

    def find_all_published(self) -> List[Event]:
        models = self._session.query(EventModel).filter(
            EventModel.status == EventStatus.PUBLISHED.value
        ).all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: EventModel) -> Event:
        event = Event(
            id=EventId(model.id),
            name=model.name,
            description=model.description,
            start_date=model.start_date,
            end_date=model.end_date,
            location=model.location,
            max_capacity=model.max_capacity,
            organizer_id=model.organizer_id,
            status=EventStatus(model.status),
        )
        for cat in model.ticket_categories:
            category = TicketCategory(
                id=TicketCategoryId(cat.id),
                event_id=EventId(cat.event_id),
                name=cat.name,
                price=Money(amount=cat.price_amount, currency=cat.price_currency),
                quota=cat.quota,
                booked_count=cat.booked_count,
                sales_start_date=cat.sales_start_date,
                sales_end_date=cat.sales_end_date,
                status=TicketCategoryStatus(cat.status),
            )
            event.ticket_categories.append(category)
        return event