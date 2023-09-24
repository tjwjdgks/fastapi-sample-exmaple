from enum import Enum


class OrderStatus(Enum):
    PAYED = "PAYED"  # 결제
    CANCELED = "CANCELED"  # 취소
