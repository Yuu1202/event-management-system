from dataclasses import dataclass


@dataclass
class RequestRefundCommand:
    booking_id: str
    customer_id: str


@dataclass
class ApproveRefundCommand:
    refund_id: str
    organizer_id: str


@dataclass
class RejectRefundCommand:
    refund_id: str
    organizer_id: str
    reason: str


@dataclass
class MarkRefundPaidOutCommand:
    refund_id: str
    payment_reference: str