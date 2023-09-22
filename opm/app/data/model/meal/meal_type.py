from enum import Enum


class MealType(str, Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    snacks = "Snacks"