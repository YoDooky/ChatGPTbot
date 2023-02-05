from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    tg_fname: str
    minute_balance: int


ololo = User(tg_id=1, tg_fname="Ololo", minute_balance=100)

data_dict = {}
for each in ololo.__annotations__:
    data_dict[each] = ololo.__getattribute__(each)
print(data_dict)


