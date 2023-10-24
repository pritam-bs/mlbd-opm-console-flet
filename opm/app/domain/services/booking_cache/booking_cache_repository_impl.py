from typing import Dict, List
from ....domain.entities.booking_entity import BookingEntity
from ....domain.entities.booking_update_entity import BookingUpdateListEntity, BookingUpdateActionEntity
from ....domain.services.booking_cache.booking_cache_repository import BookingCacheRepository
from ....domain.entities.meal_entity_type import MealEntityType
from loguru import logger


class BookingCacheRepositoryImpl(BookingCacheRepository):

    def __init__(self) -> None:
        self.bookings_map = {}

    def make_cache(self, bookings: List[BookingEntity]):
        self.bookings_map = self._create_mapping(booking_entities=bookings)

    def get_all_bookings(self) -> Dict[str, BookingEntity]:
        return self.bookings_map

    def update_cache(self, booking_updates: BookingUpdateListEntity):
        for update in booking_updates.booking_update_list:
            action = update.action
            booking_update_info = update.booking_update_info
            employee_id = booking_update_info.employee_id
            if action == BookingUpdateActionEntity.delete.value:
                try:
                    del self.bookings_map[employee_id]
                except KeyError:
                    logger.debug(
                        f"No bookin for employee_id {employee_id} found in the list.")
            elif action == BookingUpdateActionEntity.update.value:
                booking_entity = BookingEntity(
                    name=booking_update_info.name,
                    email=booking_update_info.email,
                    employee_id=booking_update_info.employee_id,
                    is_emergency=booking_update_info.is_emergency,
                    booked_meals=[MealEntityType[meal.name]
                                  for meal in booking_update_info.booked_meals] if booking_update_info.booked_meals is not None else [],
                    consumed_meals=[MealEntityType[meal.name]
                                    for meal in booking_update_info.consumed_meals] if booking_update_info.consumed_meals is not None else [],
                )
                self.bookings_map[employee_id] = booking_entity
                logger.debug(f"Booking cache updated")

    def _create_mapping(self, booking_entities: List[BookingEntity]) -> Dict[str, BookingEntity]:
        return {entity.employee_id: entity for entity in booking_entities}
