# Domain Model Draft

## Aggregates & Entities

### Aggregate: Event
- **Root Entity:** Event
  - id: EventId
  - name: String
  - description: String
  - start_date: Date
  - end_date: Date
  - location: String
  - max_capacity: Integer
  - organizer_id: String
  - status: EventStatus (Draft, Published, Cancelled, Completed)
- **Entity:** TicketCategory
  - id: TicketCategoryId
  - name: String
  - price: Money
  - quota: Integer
  - booked_count: Integer
  - sales_start_date: Date
  - sales_end_date: Date
  - status: TicketCategoryStatus (Active, Inactive)

### Aggregate: Booking
- **Root Entity:** Booking
  - id: BookingId
  - event_id: EventId
  - customer_id: String
  - ticket_category_id: TicketCategoryId
  - quantity: Integer
  - unit_price: Money
  - service_fee: Money
  - total_price: Money (derived)
  - payment_deadline: DateTime
  - status: BookingStatus (PendingPayment, Paid, Expired, Refunded)
- **Entity:** Ticket
  - id: TicketId
  - booking_id: BookingId
  - event_id: EventId
  - ticket_code: TicketCode
  - status: TicketStatus (Active, CheckedIn, Cancelled, RefundRequired)

### Aggregate: Refund
- **Root Entity:** Refund
  - id: RefundId
  - booking_id: BookingId
  - amount: Money
  - status: RefundStatus (Requested, Approved, Rejected, PaidOut)
  - rejection_reason: String (optional)
  - payment_reference: String (optional)

---

## Value Objects
| Value Object | Fields |
|---|---|
| Money | amount: Decimal, currency: String |
| TicketCode | value: String (12 char unique) |
| EventId | value: UUID |
| BookingId | value: UUID |
| TicketCategoryId | value: UUID |
| TicketId | value: UUID |
| RefundId | value: UUID |

---

## Domain Events
| Event | Trigger |
|---|---|
| EventCreated | Event organizer creates a new event |
| EventPublished | Event organizer publishes an event |
| EventCancelled | Event organizer cancels an event |
| TicketCategoryCreated | Ticket category added to event |
| TicketCategoryDisabled | Ticket category disabled |
| TicketReserved | Customer creates a booking |
| BookingPaid | Customer pays for booking |
| BookingExpired | Payment deadline passed |
| TicketCheckedIn | Gate officer checks in a ticket |
| RefundRequested | Customer requests refund |
| RefundApproved | Organizer approves refund |
| RefundRejected | Organizer rejects refund |
| RefundPaidOut | Admin marks refund as paid out |

---

## Business Rules Summary

### Event
- End date cannot be earlier than start date
- Max capacity must be greater than zero
- Event must have at least one active ticket category to be published
- Total ticket quota cannot exceed max capacity
- Cancelled event cannot be published
- Completed event cannot be cancelled

### Ticket Category
- Price cannot be negative
- Quota must be greater than zero
- Sales period must end before or at event start date
- Total quota of all categories cannot exceed event max capacity

### Booking
- Can only be created for Published events
- Can only be created within ticket sales period
- Quantity must be greater than zero
- Quantity cannot exceed remaining quota
- Customer cannot have more than one active booking per event
- Payment deadline is 15 minutes after booking created
- Payment amount must match total price
- Cannot pay after payment deadline
- Paid booking cannot expire

### Ticket
- Issued only after booking is paid
- Each ticket has a unique ticket code
- Checked-in ticket cannot be checked in again
- Check-in only on event day

### Refund
- Can only be requested for Paid bookings
- Cannot be requested if any ticket already checked in
- Can only be approved/rejected if status is Requested
- Rejection must include a reason
- Can only be paid out if status is Approved