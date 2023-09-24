from dataclasses import dataclass


@dataclass
class AccountDto:

    id: str
    bank_id: str
    is_use: str = "T"
