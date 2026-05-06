from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "IDR"

    def _post_init_(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> "Money":
        return Money(self.amount * Decimal(factor), self.currency)

    def _eq_(self, other):
        return isinstance(other, Money) and self.amount == other.amount and self.currency == other.currency


@dataclass(frozen=True)
class TicketCode:
    value: str

    def _post_init_(self):
        if not self.value or len(self.value) < 6:
            raise ValueError("TicketCode must be at least 6 characters")

    @staticmethod
    def generate() -> "TicketCode":
        return TicketCode(value=str(uuid4()).replace("-", "").upper()[:12])


@dataclass(frozen=True)
class EventId:
    value: str

    @staticmethod
    def generate() -> "EventId":
        return EventId(value=str(uuid4()))


@dataclass(frozen=True)
class BookingId:
    value: str

    @staticmethod
    def generate() -> "BookingId":
        return BookingId(value=str(uuid4()))


@dataclass(frozen=True)
class TicketCategoryId:
    value: str

    @staticmethod
    def generate() -> "TicketCategoryId":
        return TicketCategoryId(value=str(uuid4()))


@dataclass(frozen=True)
class RefundId:
    value: str

    @staticmethod
    def generate() -> "RefundId":
        return RefundId(value=str(uuid4()))


@dataclass(frozen=True)
class TicketId:
    value: str

    @staticmethod
    def generate() -> "TicketId":
        return TicketId(value=str(uuid4()))