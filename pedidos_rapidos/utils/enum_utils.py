from enum import Enum


class OrderState(str, Enum):
    TO_CONFIRM = "TO_CONFIRM"
    CONFIRMED = "CONFIRMED"
    IN_PREPARATION = "IN_PREPARATION"
    UNDER_WAY = "UNDER_WAY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"