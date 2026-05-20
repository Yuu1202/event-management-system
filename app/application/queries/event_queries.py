from dataclasses import dataclass
from typing import Optional


@dataclass
class GetPublishedEventsQuery:
    location: Optional[str] = None
    date_filter: Optional[str] = None


@dataclass
class GetEventDetailQuery:
    event_id: str


@dataclass
class GetSalesReportQuery:
    event_id: str
    organizer_id: str


@dataclass
class GetParticipantsQuery:
    event_id: str
    organizer_id: str
