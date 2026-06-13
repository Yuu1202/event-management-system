from datetime import date
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.commands.event_commands import (
    CancelEventCommand, CreateEventCommand, CreateTicketCategoryCommand,
    DisableTicketCategoryCommand, PublishEventCommand
)
from app.application.queries.event_queries import (
    GetEventDetailQuery, GetParticipantsQuery,
    GetPublishedEventsQuery, GetSalesReportQuery
)
from app.presentation.dependencies.dependencies import (
    get_cancel_event_handler, get_create_event_handler,
    get_create_ticket_category_handler, get_disable_ticket_category_handler,
    get_event_detail_handler, get_participants_handler,
    get_published_events_handler, get_publish_event_handler,
    get_sales_report_handler
)

router = APIRouter(prefix="/events", tags=["Events"])


class CreateEventRequest(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    location: str
    max_capacity: int
    organizer_id: str


class CreateTicketCategoryRequest(BaseModel):
    name: str
    price: Decimal
    quota: int
    sales_start_date: date
    sales_end_date: date
    organizer_id: str


@router.post("", status_code=201)
def create_event(
    body: CreateEventRequest,
    handler=Depends(get_create_event_handler)
):
    try:
        event_id = handler.handle(CreateEventCommand(
            name=body.name,
            description=body.description,
            start_date=body.start_date,
            end_date=body.end_date,
            location=body.location,
            max_capacity=body.max_capacity,
            organizer_id=body.organizer_id,
        ))
        return {"event_id": event_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{event_id}/publish", status_code=200)
def publish_event(
    event_id: str,
    organizer_id: str,
    handler=Depends(get_publish_event_handler)
):
    try:
        handler.handle(PublishEventCommand(event_id=event_id, organizer_id=organizer_id))
        return {"message": "Event published successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{event_id}/cancel", status_code=200)
def cancel_event(
    event_id: str,
    organizer_id: str,
    handler=Depends(get_cancel_event_handler)
):
    try:
        handler.handle(CancelEventCommand(event_id=event_id, organizer_id=organizer_id))
        return {"message": "Event cancelled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{event_id}/categories", status_code=201)
def create_ticket_category(
    event_id: str,
    body: CreateTicketCategoryRequest,
    handler=Depends(get_create_ticket_category_handler)
):
    try:
        category_id = handler.handle(CreateTicketCategoryCommand(
            event_id=event_id,
            name=body.name,
            price=body.price,
            quota=body.quota,
            sales_start_date=body.sales_start_date,
            sales_end_date=body.sales_end_date,
            organizer_id=body.organizer_id,
        ))
        return {"category_id": category_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{event_id}/categories/{category_id}/disable", status_code=200)
def disable_ticket_category(
    event_id: str,
    category_id: str,
    organizer_id: str,
    handler=Depends(get_disable_ticket_category_handler)
):
    try:
        handler.handle(DisableTicketCategoryCommand(
            event_id=event_id,
            category_id=category_id,
            organizer_id=organizer_id,
        ))
        return {"message": "Ticket category disabled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def get_published_events(
    location: Optional[str] = None,
    date_filter: Optional[str] = None,
    handler=Depends(get_published_events_handler)
):
    result = handler.handle(GetPublishedEventsQuery(location=location, date_filter=date_filter))
    return result


@router.get("/{event_id}")
def get_event_detail(
    event_id: str,
    handler=Depends(get_event_detail_handler)
):
    try:
        return handler.handle(GetEventDetailQuery(event_id=event_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{event_id}/report")
def get_sales_report(
    event_id: str,
    organizer_id: str,
    handler=Depends(get_sales_report_handler)
):
    try:
        return handler.handle(GetSalesReportQuery(event_id=event_id, organizer_id=organizer_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{event_id}/participants")
def get_participants(
    event_id: str,
    organizer_id: str,
    handler=Depends(get_participants_handler)
):
    try:
        return handler.handle(GetParticipantsQuery(event_id=event_id, organizer_id=organizer_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))