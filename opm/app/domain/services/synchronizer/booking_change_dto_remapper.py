from ....data.model.synchronizer.booking_change_dto import BookingChangeDTO
from ....domain.entities.booking_change_entity import BookingChangeEntity


class BookingChangeRemapper:
    @staticmethod
    def map_from(booking_change_dto: BookingChangeDTO):
        return BookingChangeEntity(
            employee_id=booking_change_dto.employee_id)

    @staticmethod
    def map_to(booking_change_entity: BookingChangeEntity):
        return BookingChangeDTO(
            employee_id=booking_change_entity.employee_id)
