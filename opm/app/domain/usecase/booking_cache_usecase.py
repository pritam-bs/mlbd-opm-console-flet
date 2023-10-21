from ...domain.services.booking_cache.booking_cache_repository import BookingCacheRepository
from ...domain.entities.booking_entity import BookingEntity
from ...domain.entities.booking_update_entity import BookingUpdateListEntity
from typing import Dict


class BookingCacheUsecase:
    def __init__(self, booking_cache_repository: BookingCacheRepository) -> None:
        self.booking_cache_repository = booking_cache_repository

    def get_cached_booking(self) -> Dict[str, BookingEntity]:
        return self.booking_cache_repository.get_all_bookings()

    def update_cached_booking(self, booking_updates: BookingUpdateListEntity):
        self.booking_cache_repository.update_cache(
            booking_updates=booking_updates)
