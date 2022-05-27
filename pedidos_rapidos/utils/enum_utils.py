from enum import Enum


class OrderState(Enum):
    TO_CONFIRM = 1
    CONFIRMED = 2
    IN_PREPARATION = 3
    UNDER_WAY = 4
    DELIVERED = 5
    CANCELLED = 6

