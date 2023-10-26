from ....data.model.synchronizer.booking_update_dto import (
    BookingUpdateDTO,
    BookingUpdateListDTO,
)
from ...entities.booking_update_entity import (
    BookingUpdateEntity,
    BookingUpdateInfoEntity,
    BookingUpdateListEntity
)


class BookingUpdateRemapper:
    @staticmethod
    def map(booking_update_dto: BookingUpdateDTO):
        booking_data = booking_update_dto.booking_data
        booking_update_info = BookingUpdateInfoEntity(
            name=booking_data.name,
            email=booking_data.email,
            employee_id=booking_data.employee_id,
            booked_meals=booking_data.booked_meals,
            consumed_meals=booking_data.consumed_meals,
            is_emergency=booking_data.is_emergency
        )
        return BookingUpdateEntity(
            action=booking_update_dto.action,
            booking_update_info=booking_update_info
        )

    @staticmethod
    def map_sqs_dto(booking_update_list_dto: BookingUpdateListDTO):
        booking_update_list = [BookingUpdateRemapper.map(booking_update_dto)
                               for booking_update_dto in booking_update_list_dto.booking_update_list]
        entitie = BookingUpdateListEntity(
            booking_update_list=booking_update_list)
        return entitie
