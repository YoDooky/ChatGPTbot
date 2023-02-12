from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    tg_username: str
    tg_fname: str
    tg_lname: str
    timestamp: str


@dataclass
class Payment:
    buyer_id: int
    usage_expiring: str
    money_spent: int
    last_bill_id: str
    payment_message_id: int
    timestamp: str
