from app.application.interfaces.notification_service import NotificationServiceInterface


class MockNotificationService(NotificationServiceInterface):

    def send_booking_confirmation(self, customer_id: str, booking_id: str) -> None:
        print(f"[MockNotificationService] Booking confirmation sent to customer {customer_id} for booking {booking_id}")

    def send_payment_confirmation(self, customer_id: str, booking_id: str) -> None:
        print(f"[MockNotificationService] Payment confirmation sent to customer {customer_id} for booking {booking_id}")

    def send_refund_notification(self, customer_id: str, refund_id: str, status: str) -> None:
        print(f"[MockNotificationService] Refund {status} notification sent to customer {customer_id} for refund {refund_id}")

    def send_event_cancellation_notice(self, customer_id: str, event_id: str) -> None:
        print(f"[MockNotificationService] Event cancellation notice sent to customer {customer_id} for event {event_id}")
