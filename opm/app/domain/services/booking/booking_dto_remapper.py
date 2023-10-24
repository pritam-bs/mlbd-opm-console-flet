from ....data.model.booking.booking_dto import BookingDTO, BookingStatus
from ....domain.entities.booking_entity import BookingEntity
from ....domain.entities.meal_entity_type import MealEntityType


class BookingRemapper:
    @staticmethod
    def map(booking: BookingStatus):
        return BookingEntity(
            booking.name,
            booking.email,
            booking.employee_id,
            booking.is_emergency,
            [MealEntityType[meal.name]
                for meal in booking.booked_meals] if booking.booked_meals is not None else [],
            [MealEntityType[meal.name]
                for meal in booking.consumed_meals] if booking.consumed_meals is not None else []
        )

    @staticmethod
    def map_network_dto(booking_dto: BookingDTO):
        entities = [BookingRemapper.map(booking)
                    for booking in booking_dto.bookings]
        return entities
