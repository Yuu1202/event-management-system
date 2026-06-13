from typing import Optional
from sqlalchemy.orm import Session

from app.domain.aggregates.refund import Refund, RefundStatus
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.value_objects import BookingId, Money, RefundId
from app.infrastructure.database.models import RefundModel


class SQLAlchemyRefundRepository(RefundRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, refund: Refund) -> None:
        model = self._session.get(RefundModel, refund.id.value)
        if model is None:
            model = RefundModel(id=refund.id.value)
            self._session.add(model)

        model.booking_id = refund.booking_id.value
        model.amount_value = refund.amount.amount
        model.amount_currency = refund.amount.currency
        model.status = refund.status.value
        model.rejection_reason = refund.rejection_reason
        model.payment_reference = refund.payment_reference

        self._session.commit()

    def find_by_id(self, refund_id: RefundId) -> Optional[Refund]:
        model = self._session.get(RefundModel, refund_id.value)
        return self._to_domain(model) if model else None

    def find_by_booking_id(self, booking_id: BookingId) -> Optional[Refund]:
        model = self._session.query(RefundModel).filter(
            RefundModel.booking_id == booking_id.value
        ).first()
        return self._to_domain(model) if model else None

    def _to_domain(self, model: RefundModel) -> Refund:
        refund = Refund(
            id=RefundId(model.id),
            booking_id=BookingId(model.booking_id),
            amount=Money(amount=model.amount_value, currency=model.amount_currency),
            status=RefundStatus(model.status),
            rejection_reason=model.rejection_reason,
            payment_reference=model.payment_reference,
        )
        return refund
