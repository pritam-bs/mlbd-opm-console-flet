from ....data.model.booking.booking_dto import BookingDTO, BookingStatus
from ....domain.entities.booking_entity import BookingEntity


class BookingRemapper:
    @staticmethod
    def map(booking: BookingStatus):
        return BookingEntity(
            booking.name,
            booking.email,
            booking.employee_id,
            booking.is_emergency,
            booking.booked_meals,
            booking.consumed_meals
        )

    @staticmethod
    def map_network_dto(booking_dto: BookingDTO):
        entities = [BookingRemapper.map(booking)
                    for booking in booking_dto.bookings]
        return entities
