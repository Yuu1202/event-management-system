from app.application.commands.refund_commands import (
    ApproveRefundCommand, MarkRefundPaidOutCommand,
    RejectRefundCommand, RequestRefundCommand
)
from app.application.interfaces.notification_service import NotificationServiceInterface
from app.application.interfaces.refund_payment_service import RefundPaymentServiceInterface
from app.domain.aggregates.refund import Refund
from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.value_objects import BookingId, RefundId


class RequestRefundHandler:
    def __init__(self, booking_repo: BookingRepository, refund_repo: RefundRepository):
        self._booking_repo = booking_repo
        self._refund_repo = refund_repo

    def handle(self, command: RequestRefundCommand) -> str:
        booking = self._booking_repo.find_by_id(BookingId(command.booking_id))
        if booking is None:
            raise ValueError("Booking not found")
        if booking.customer_id != command.customer_id:
            raise ValueError("Unauthorized")
        if booking.has_checked_in_ticket():
            raise ValueError("Cannot request refund: ticket already checked in")
        refund = Refund.create(booking_id=booking.id, amount=booking.total_price)
        self._refund_repo.save(refund)
        return refund.id.value


class ApproveRefundHandler:
    def __init__(
        self,
        refund_repo: RefundRepository,
        booking_repo: BookingRepository,
        notification_service: NotificationServiceInterface,
    ):
        self._refund_repo = refund_repo
        self._booking_repo = booking_repo
        self._notification_service = notification_service

    def handle(self, command: ApproveRefundCommand) -> None:
        refund = self._refund_repo.find_by_id(RefundId(command.refund_id))
        if refund is None:
            raise ValueError("Refund not found")
        booking = self._booking_repo.find_by_id(refund.booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        refund.approve()
        booking.cancel_tickets()
        booking.mark_refunded()
        self._refund_repo.save(refund)
        self._booking_repo.save(booking)
        self._notification_service.send_refund_notification(
            booking.customer_id, refund.id.value, "Approved"
        )


class RejectRefundHandler:
    def __init__(
        self,
        refund_repo: RefundRepository,
        booking_repo: BookingRepository,
        notification_service: NotificationServiceInterface,
    ):
        self._refund_repo = refund_repo
        self._booking_repo = booking_repo
        self._notification_service = notification_service

    def handle(self, command: RejectRefundCommand) -> None:
        refund = self._refund_repo.find_by_id(RefundId(command.refund_id))
        if refund is None:
            raise ValueError("Refund not found")
        booking = self._booking_repo.find_by_id(refund.booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        refund.reject(command.reason)
        self._refund_repo.save(refund)
        self._notification_service.send_refund_notification(
            booking.customer_id, refund.id.value, "Rejected"
        )


class MarkRefundPaidOutHandler:
    def __init__(
        self,
        refund_repo: RefundRepository,
        refund_payment_service: RefundPaymentServiceInterface,
    ):
        self._refund_repo = refund_repo
        self._refund_payment_service = refund_payment_service

    def handle(self, command: MarkRefundPaidOutCommand) -> None:
        refund = self._refund_repo.find_by_id(RefundId(command.refund_id))
        if refund is None:
            raise ValueError("Refund not found")
        self._refund_payment_service.process_refund(
            refund.id.value, refund.amount.amount, refund.amount.currency
        )
        refund.mark_paid_out(command.payment_reference)
        self._refund_repo.save(refund)