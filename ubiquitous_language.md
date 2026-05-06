# Ubiquitous Language Glossary

| Term | Meaning |
|---|---|
| Event | An activity organized by an Event Organizer and attended by Customers. Has a name, description, date, location, and maximum capacity. |
| Event Organizer | A user who creates, manages, and publishes Events. Can approve or reject Refund requests. |
| Customer | A user who browses Events, creates Bookings, pays for Tickets, and can request Refunds. |
| Gate Officer | A user who validates Tickets during event check-in. |
| System Admin | A user who triggers Refund payouts and monitors operational processes. |
| Ticket Category | A type of ticket within an Event (e.g., Regular, VIP, Early Bird). Has a name, price, quota, and sales period. |
| Quota | The maximum number of Tickets available within a Ticket Category. |
| Remaining Quota | Quota minus the number of tickets already reserved or sold. |
| Sales Period | The date range during which a Ticket Category can be purchased. Defined by sales start date and sales end date. |
| Booking | A temporary reservation created by a Customer before payment is completed. Has a payment deadline. |
| PendingPayment | A Booking status indicating payment has not been completed. |
| Paid | A Booking status indicating payment has been successfully completed. |
| Expired | A Booking status indicating the payment deadline has passed without payment. |
| Refunded | A Booking status indicating a Refund has been approved for this Booking. |
| Payment Deadline | The deadline for completing payment after a Booking is created. Default is 15 minutes. |
| Ticket | Proof of attendance generated after a Booking is Paid. Each Booking issues one Ticket per quantity. |
| Ticket Code | A unique alphanumeric code used to identify and validate a Ticket during check-in. |
| Active | A Ticket status indicating the ticket is valid and has not been used. |
| CheckedIn | A Ticket status indicating the participant has entered the event venue. |
| Cancelled | A Ticket status indicating the ticket has been cancelled (e.g., due to an approved Refund). |
| RefundRequired | A Ticket status indicating the ticket requires a refund due to event cancellation. |
| Check-in | The process of validating a Ticket when a participant enters the event venue. Can only be done on event day. |
| Refund | The process of returning money to a Customer. Goes through Requested → Approved → PaidOut flow. |
| Requested | A Refund status indicating the Customer has submitted a refund request. |
| Approved | A Refund status indicating the Event Organizer has approved the refund. |
| Rejected | A Refund status indicating the Event Organizer has rejected the refund. Must include a rejection reason. |
| PaidOut | A Refund status indicating the refund money has been sent to the Customer. |
| Money | A value object representing an amount and currency. Cannot be negative. |
| Domain Event | A record of something significant that happened in the domain (e.g., EventCreated, BookingPaid). |
| Aggregate | A cluster of domain objects treated as a single unit (Event, Booking, Refund). |
| Repository | An interface for storing and retrieving Aggregates. |
| Payment Gateway | An external system used to process Booking payments. |
| Refund Payment Service | An external system used to process Refund payouts to Customers. |
| Notification Service | An external system used to send email or WhatsApp notifications. |