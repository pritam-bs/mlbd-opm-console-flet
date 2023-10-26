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
        console_booking_resource = booking_update_dto.console_booking_resource
        booking_update_info = BookingUpdateInfoEntity(
            name=console_booking_resource.name,
            email=console_booking_resource.email,
            employee_id=console_booking_resource.employee_id,
            booked_meals=console_booking_resource.booked_meals,
            consumed_meals=console_booking_resource.consumed_meals,
            is_emergency=console_booking_resource.is_emergency
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
