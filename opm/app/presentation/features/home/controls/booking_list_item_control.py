from flet import (
    Row,
    Card,
    UserControl,
    Container,
    Column,
    Text,
    colors,
    TextThemeStyle,
    border,
    alignment,
    MainAxisAlignment,
)

from .....domain.entities.booking_entity import BookingEntity


class BookingListItemControl(UserControl):
    def __init__(
        self,
        booking_entity: BookingEntity
    ):
        super().__init__()
        self.is_mounted = False
        self.booking_entiry = booking_entity

    async def did_mount_async(self):
        self.is_mounted = True
        await super().did_mount_async()

    async def will_unmount_async(self):
        self.is_mounted = False
        await super().will_unmount_async()

    def build(self):
        _meal_row = Row()
        if self.booking_entiry.booked_meals is not None and len(self.booking_entiry.booked_meals) > 0:
            for booked_meal in self.booking_entiry.booked_meals:
                bgcolor = colors.TRANSPARENT
                if self.booking_entiry.is_consumed(meal=booked_meal):
                    bgcolor = colors.SECONDARY_CONTAINER
                meal = Container(
                    content=Text(booked_meal.value,
                                 style=TextThemeStyle.LABEL_MEDIUM),
                    border=border.all(
                        width=1, color=colors.ON_PRIMARY_CONTAINER),
                    padding=4,
                    border_radius=4,
                    bgcolor=bgcolor,
                )
                _meal_row.controls.append(meal)
        else:
            _meal_row.visible = False

        return Card(
            content=Container(
                content=Column(
                    controls=[
                        Text(self.booking_entiry.name),
                        _meal_row,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                padding=10,
                alignment=alignment.center_left
            ),
        )
