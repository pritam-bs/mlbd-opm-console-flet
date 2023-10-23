import asyncio
from ....domain.services.scheduler.booking_update_scheduler_repository import ScheduledBookingUpdateFunc, BookingUpdateSchedulerRepository
from ....domain.services.booking.booking_repository import BookingRepository
import schedule
from ....settings.settings import settings


class BookingUpdateSchedulerRepositoryImpl(BookingUpdateSchedulerRepository):
    def __init__(self, booking_repository: BookingRepository) -> None:
        self.booking_repository = booking_repository
        self.interval = settings.booking_update_check_interval

    def __del__(self):
        self.stop()

    def start(self, on_booking_update: ScheduledBookingUpdateFunc):
        self.on_booking_update = on_booking_update
        # Schedule the job to run at specific times
        morning_booking_update_schedule = settings.morning_booking_update_schedule
        midday_booking_update_schedule = settings.midday_booking_update_schedule
        midnight_booking_update_schedule = settings.midnight_booking_update_schedule
        schedule.every().day.at(morning_booking_update_schedule).do(self._run_job)
        schedule.every().day.at(midday_booking_update_schedule).do(self._run_job)
        schedule.every().day.at(midnight_booking_update_schedule).do(self._run_job)
        self._stop_signal = False
        self._timer_task = asyncio.create_task(self._repetitive_task())

    def stop(self):
        self._stop_signal = True
        schedule.clear()
        if self._timer_task is not None:
            self._timer_task.cancel()
        if self._get_booking_task is not None:
            self._get_booking_task.cancel()

    def _run_job(self):
        self._get_booking_task = asyncio.create_task(self._get_bookings())

    async def _get_bookings(self):
        booking_list = await asyncio.create_task(self.booking_repository.get_all_bookings())
        await self.on_booking_update(booking_list)

    async def _repetitive_task(self):
        while not self._stop_signal:
            schedule.run_pending()
            await asyncio.sleep(self.interval)
