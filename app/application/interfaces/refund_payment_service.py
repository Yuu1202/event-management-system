from abc import ABC, abstractmethod
from decimal import Decimal


class RefundPaymentServiceInterface(ABC):

    @abstractmethod
    def process_refund(self, refund_id: str, amount: Decimal, currency: str) -> str:
        pass