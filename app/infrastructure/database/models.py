from datetime import date, datetime
from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class EventModel(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    organizer_id = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Draft")

    ticket_categories = relationship("TicketCategoryModel", back_populates="event", cascade="all, delete-orphan")


class TicketCategoryModel(Base):
    __tablename__ = "ticket_categories"

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)
    price_amount = Column(Numeric, nullable=False)
    price_currency = Column(String, nullable=False, default="IDR")
    quota = Column(Integer, nullable=False)
    booked_count = Column(Integer, nullable=False, default=0)
    sales_start_date = Column(Date, nullable=False)
    sales_end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="Active")

    event = relationship("EventModel", back_populates="ticket_categories")


class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    customer_id = Column(String, nullable=False)
    ticket_category_id = Column(String, ForeignKey("ticket_categories.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price_amount = Column(Numeric, nullable=False)
    unit_price_currency = Column(String, nullable=False, default="IDR")
    service_fee_amount = Column(Numeric, nullable=False, default=0)
    service_fee_currency = Column(String, nullable=False, default="IDR")
    payment_deadline = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="PendingPayment")

    tickets = relationship("TicketModel", back_populates="booking", cascade="all, delete-orphan")


class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True)
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    ticket_code = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False, default="Active")

    booking = relationship("BookingModel", back_populates="tickets")


class RefundModel(Base):
    __tablename__ = "refunds"

    id = Column(String, primary_key=True)
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)
    amount_value = Column(Numeric, nullable=False)
    amount_currency = Column(String, nullable=False, default="IDR")
    status = Column(String, nullable=False, default="Requested")
    rejection_reason = Column(Text, nullable=True)
    payment_reference = Column(String, nullable=True)