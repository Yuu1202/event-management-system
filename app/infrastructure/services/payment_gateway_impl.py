from decimal import Decimal
from app.application.interfaces.payment_gateway import PaymentGatewayInterface


class MockPaymentGateway(PaymentGatewayInterface):

    def process_payment(self, booking_id: str, amount: Decimal, currency: str) -> bool:
        print(f"[MockPaymentGateway] Payment processed for booking {booking_id}: {amount} {currency}")
        return True

    def get_payment_status(self, booking_id: str) -> str:
        print(f"[MockPaymentGateway] Payment status for booking {booking_id}: SUCCESS")
        return "SUCCESS"
