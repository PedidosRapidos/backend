from enum import Enum

formats = {
    "TO_CONFIRM": "To Confirm",
    "CONFIRMED": "Confirmed",
    "IN_PREPARATION": "In preparation",
    "UNDER_WAY": "Under way",
    "DELIVERED": "Delivered",
    "CANCELLED": "Cancelled",
}


class OrderState(str, Enum):
    TO_CONFIRM = "TO_CONFIRM"
    CONFIRMED = "CONFIRMED"
    IN_PREPARATION = "IN_PREPARATION"
    UNDER_WAY = "UNDER_WAY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

    def format(self):
        return formats[self.value]
