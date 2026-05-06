from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.aggregates.event import Event
from app.domain.value_objects import EventId


class EventRepository(ABC):

    @abstractmethod
    def save(self, event: Event) -> None:
        pass

    @abstractmethod
    def find_by_id(self, event_id: EventId) -> Optional[Event]:
        pass

    @abstractmethod
    def find_all_published(self) -> List[Event]:
        pass