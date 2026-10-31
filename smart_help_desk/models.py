from dataclasses import dataclass


# ==================================================
# DATA MODEL
# ==================================================

@dataclass
class Ticket:
    id: int
    title: str
    description: str
    category: str
    status: str = "Open"
