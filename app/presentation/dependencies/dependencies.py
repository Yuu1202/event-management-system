from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.handlers.booking_handlers import (
    CreateBookingHandler, ExpireBookingHandler,
    GetBookingTicketsHandler, PayBookingHandler
)
from app.application.handlers.event_handlers import (
    CancelEventHandler, CreateEventHandler, CreateTicketCategoryHandler,
    DisableTicketCategoryHandler, GetEventDetailHandler,
    GetParticipantsHandler, GetPublishedEventsHandler,
    GetSalesReportHandler, PublishEventHandler
)
from app.application.handlers.refund_handlers import (
    ApproveRefundHandler, MarkRefundPaidOutHandler,
    RejectRefundHandler, RequestRefundHandler
)
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.booking_repository_impl import SQLAlchemyBookingRepository
from app.infrastructure.repositories.event_repository_impl import SQLAlchemyEventRepository
from app.infrastructure.repositories.refund_repository_impl import SQLAlchemyRefundRepository
from app.infrastructure.services.notification_service_impl import MockNotificationService
from app.infrastructure.services.payment_gateway_impl import MockPaymentGateway
from app.infrastructure.services.refund_payment_service_impl import MockRefundPaymentService


def get_event_repo(db: Session = Depends(get_db)):
    return SQLAlchemyEventRepository(db)


def get_booking_repo(db: Session = Depends(get_db)):
    return SQLAlchemyBookingRepository(db)


def get_refund_repo(db: Session = Depends(get_db)):
    return SQLAlchemyRefundRepository(db)


def get_payment_gateway():
    return MockPaymentGateway()


def get_refund_payment_service():
    return MockRefundPaymentService()


def get_notification_service():
    return MockNotificationService()


# Event Handlers
def get_create_event_handler(event_repo=Depends(get_event_repo)):
    return CreateEventHandler(event_repo)

def get_publish_event_handler(event_repo=Depends(get_event_repo)):
    return PublishEventHandler(event_repo)

def get_cancel_event_handler(event_repo=Depends(get_event_repo)):
    return CancelEventHandler(event_repo)

def get_create_ticket_category_handler(event_repo=Depends(get_event_repo)):
    return CreateTicketCategoryHandler(event_repo)

def get_disable_ticket_category_handler(event_repo=Depends(get_event_repo)):
    return DisableTicketCategoryHandler(event_repo)

def get_published_events_handler(event_repo=Depends(get_event_repo)):
    return GetPublishedEventsHandler(event_repo)

def get_event_detail_handler(event_repo=Depends(get_event_repo)):
    return GetEventDetailHandler(event_repo)

def get_sales_report_handler(
    event_repo=Depends(get_event_repo),
    booking_repo=Depends(get_booking_repo)
):
    return GetSalesReportHandler(event_repo, booking_repo)

def get_participants_handler(booking_repo=Depends(get_booking_repo)):
    return GetParticipantsHandler(booking_repo)


# Booking Handlers
def get_create_booking_handler(
    event_repo=Depends(get_event_repo),
    booking_repo=Depends(get_booking_repo)
):
    return CreateBookingHandler(event_repo, booking_repo)

def get_pay_booking_handler(
    booking_repo=Depends(get_booking_repo),
    payment_gateway=Depends(get_payment_gateway),
    notification_service=Depends(get_notification_service)
):
    return PayBookingHandler(booking_repo, payment_gateway, notification_service)

def get_expire_booking_handler(
    booking_repo=Depends(get_booking_repo),
    event_repo=Depends(get_event_repo)
):
    return ExpireBookingHandler(booking_repo, event_repo)

def get_booking_tickets_handler(booking_repo=Depends(get_booking_repo)):
    return GetBookingTicketsHandler(booking_repo)


# Refund Handlers
def get_request_refund_handler(
    booking_repo=Depends(get_booking_repo),
    refund_repo=Depends(get_refund_repo)
):
    return RequestRefundHandler(booking_repo, refund_repo)

def get_approve_refund_handler(
    refund_repo=Depends(get_refund_repo),
    booking_repo=Depends(get_booking_repo),
    notification_service=Depends(get_notification_service)
):
    return ApproveRefundHandler(refund_repo, booking_repo, notification_service)

def get_reject_refund_handler(
    refund_repo=Depends(get_refund_repo),
    booking_repo=Depends(get_booking_repo),
    notification_service=Depends(get_notification_service)
):
    return RejectRefundHandler(refund_repo, booking_repo, notification_service)

def get_mark_refund_paidout_handler(
    refund_repo=Depends(get_refund_repo),
    refund_payment_service=Depends(get_refund_payment_service)
):
    return MarkRefundPaidOutHandler(refund_repo, refund_payment_service)