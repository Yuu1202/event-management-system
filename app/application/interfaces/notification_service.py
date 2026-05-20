from abc import ABC, abstractmethod


class NotificationServiceInterface(ABC):

    @abstractmethod
    def send_booking_confirmation(self, customer_id: str, booking_id: str) -> None:
        pass

    @abstractmethod
    def send_payment_confirmation(self, customer_id: str, booking_id: str) -> None:
        pass

    @abstractmethod
    def send_refund_notification(self, customer_id: str, refund_id: str, status: str) -> None:
        pass

    @abstractmethod
    def send_event_cancellation_notice(self, customer_id: str, event_id: str) -> None:
        pass