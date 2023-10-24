from ......data.api.api_client import APIClient
from ......data.model.booking.booking_dto import BookingDTO


class BookingRemoteDatasource:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def get_all_bookings(self) -> BookingDTO:
        response = await self.api_client.path(
            '/booking-data/today'
        ).get().request()
        booking_dto = BookingDTO.from_dict(response)
        return booking_dto
