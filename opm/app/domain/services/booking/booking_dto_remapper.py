from ....data.model.booking.booking_dto import BookingDTO, BookingStatus
from ....domain.entities.booking_entity import BookingEntity


class BookingRemapper:
    @staticmethod
    def map(booking: BookingStatus):
        return BookingEntity(
            booking.employee_id,
            booking.name,
            booking.email,
            booking.booked_meals,
            booking.consumed_meals,
            booking.is_emergency
        )

    @staticmethod
    def map_network_dto(booking_dto: BookingDTO):
        entities = [BookingRemapper.map(booking)
                    for booking in booking_dto]
        return entities
