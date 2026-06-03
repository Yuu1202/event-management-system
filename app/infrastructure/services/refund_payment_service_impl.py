from decimal import Decimal
from app.application.interfaces.refund_payment_service import RefundPaymentServiceInterface


class MockRefundPaymentService(RefundPaymentServiceInterface):

    def process_refund(self, refund_id: str, amount: Decimal, currency: str) -> str:
        reference = f"MOCK-REF-{refund_id[:8].upper()}"
        print(f"[MockRefundPaymentService] Refund processed for {refund_id}: {amount} {currency} -> ref: {reference}")
        return reference
