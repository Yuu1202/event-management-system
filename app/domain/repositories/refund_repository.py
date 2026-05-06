from abc import ABC, abstractmethod
from typing import Optional

from app.domain.aggregates.refund import Refund
from app.domain.value_objects import BookingId, RefundId


class RefundRepository(ABC):

    @abstractmethod
    def save(self, refund: Refund) -> None:
        pass

    @abstractmethod
    def find_by_id(self, refund_id: RefundId) -> Optional[Refund]:
        pass

    @abstractmethod
    def find_by_booking_id(self, booking_id: BookingId) -> Optional[Refund]:
        pass