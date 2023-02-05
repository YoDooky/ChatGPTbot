from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    tg_username: str
    tg_phone: str
    tg_fname: str
    tg_lname: str
    minute_balance: int
    money_spent: int
    timestamp: str
