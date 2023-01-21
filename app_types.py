from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    tg_username: str
    tg_phone: str
    tg_fname: str
    tg_lname: str
    message: str
    timestamp: str
