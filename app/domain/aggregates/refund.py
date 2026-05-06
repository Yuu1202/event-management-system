from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

from app.domain.events import (
    DomainEvent, RefundApproved, RefundPaidOut, RefundRejected, RefundRequested
)
from app.domain.value_objects import BookingId, Money, RefundId


class RefundStatus(str, Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID_OUT = "PaidOut"


@dataclass
class Refund:
    id: RefundId
    booking_id: BookingId
    amount: Money
    status: RefundStatus = RefundStatus.REQUESTED
    rejection_reason: Optional[str] = None
    payment_reference: Optional[str] = None
    _domain_events: List[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(booking_id: BookingId, amount: Money) -> "Refund":
        refund_id = RefundId.generate()
        refund = Refund(
            id=refund_id,
            booking_id=booking_id,
            amount=amount,
        )
        refund._domain_events.append(
            RefundRequested(refund_id=refund_id.value, booking_id=booking_id.value)
        )
        return refund

    def approve(self):
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Refund can only be approved if status is Requested")
        self.status = RefundStatus.APPROVED
        self._domain_events.append(RefundApproved(refund_id=self.id.value))

    def reject(self, reason: str):
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Refund can only be rejected if status is Requested")
        if not reason:
            raise ValueError("Rejection reason must be provided")
        self.status = RefundStatus.REJECTED
        self.rejection_reason = reason
        self._domain_events.append(
            RefundRejected(refund_id=self.id.value, reason=reason)
        )

    def mark_paid_out(self, payment_reference: str):
        if self.status != RefundStatus.APPROVED:
            raise ValueError("Refund can only be paid out if status is Approved")
        self.payment_reference = payment_reference
        self.status = RefundStatus.PAID_OUT
        self._domain_events.append(
            RefundPaidOut(refund_id=self.id.value, payment_reference=payment_reference)
        )

    def pull_domain_events(self) -> List[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events