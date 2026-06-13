from dataclasses import dataclass


@dataclass
class GetBookingTicketsQuery:
    booking_id: str
    customer_id: str


@dataclass
class GetCustomerBookingsQuery:
    customer_id: str