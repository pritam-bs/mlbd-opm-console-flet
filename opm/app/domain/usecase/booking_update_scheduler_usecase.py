from ...domain.services.scheduler.booking_update_scheduler_repository import BookingUpdateSchedulerRepository, ScheduledBookingUpdateFunc


class BookingUpdateSchedulerUsecase:
    def __init__(self, booking_update_scheduler_repository: BookingUpdateSchedulerRepository) -> None:
        self.booking_update_scheduler = booking_update_scheduler_repository

    def start(self, on_scheduled_booking_update: ScheduledBookingUpdateFunc):
        self.booking_update_scheduler.start(
            on_booking_update=on_scheduled_booking_update)

    def stop(self):
        self.booking_update_scheduler.stop()
