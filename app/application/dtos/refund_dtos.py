from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RequestRefundDTO:
    booking_id: str
    customer_id: str


@dataclass
class ApproveRefundDTO:
    refund_id: str
    organizer_id: str


@dataclass
class RejectRefundDTO:
    refund_id: str
    organizer_id: str
    reason: str


@dataclass
class MarkRefundPaidOutDTO:
    refund_id: str
    payment_reference: str


@dataclass
class RefundDetailDTO:
    id: str
    booking_id: str
    amount: Decimal
    currency: str
    status: str
    rejection_reason: str = None
    payment_reference: str = None