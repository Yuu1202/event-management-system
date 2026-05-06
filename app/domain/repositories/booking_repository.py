from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.aggregates.booking import Booking
from app.domain.value_objects import BookingId, EventId


class BookingRepository(ABC):

    @abstractmethod
    def save(self, booking: Booking) -> None:
        pass

    @abstractmethod
    def find_by_id(self, booking_id: BookingId) -> Optional[Booking]:
        pass

    @abstractmethod
    def find_by_customer_and_event(self, customer_id: str, event_id: EventId) -> Optional[Booking]:
        pass

    @abstractmethod
    def find_paid_by_event(self, event_id: EventId) -> List[Booking]:
        pass