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
        consoleBookingResource = booking_update_dto.consoleBookingResource
        booking_update_info = BookingUpdateInfoEntity(
            name=consoleBookingResource.name,
            email=consoleBookingResource.email,
            employee_id=consoleBookingResource.employeeId,
            booked_meals=consoleBookingResource.bookedMeals,
            consumed_meals=consoleBookingResource.consumedMeals,
            is_emergency=consoleBookingResource.isEmergency
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
