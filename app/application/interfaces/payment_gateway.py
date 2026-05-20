from abc import ABC, abstractmethod
from decimal import Decimal


class PaymentGatewayInterface(ABC):

    @abstractmethod
    def process_payment(self, booking_id: str, amount: Decimal, currency: str) -> bool:
        pass

    @abstractmethod
    def get_payment_status(self, booking_id: str) -> str:
        pass