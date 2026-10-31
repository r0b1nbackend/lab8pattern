from itertools import count
from typing import Optional

from models import Ticket
from patterns.interpreter import QueryInterpreter
from patterns.iterator import TicketIterator
from patterns.validation import build_validation_chain


# ==================================================
# MEDIATOR PATTERN
# ==================================================

class HelpDeskMediator:
    def __init__(self):
        self._tickets = []
        self._ids = count(1)
        self.validator = build_validation_chain()

        self.add_ticket(
            "Computer will not start",
            "The computer does not turn on when I press the power button.",
            "IT",
        )

        self.add_ticket(
            "Cannot access account",
            "I cannot sign in to my university account.",
            "Account",
        )

        self.add_ticket(
            "Wi-Fi connection issue",
            "The computer cannot connect to the classroom Wi-Fi network.",
            "IT",
        )

    def add_ticket(self, title, description, category):
        data = {
            "title": title,
            "description": description,
            "category": category,
        }

        error = self.validator.handle(data)

        if error:
            raise ValueError(error)

        ticket = Ticket(
            id=next(self._ids),
            title=title.strip(),
            description=description.strip(),
            category=category,
            status="Open",
        )

        self._tickets.append(ticket)

        return ticket

    def find_ticket(self, ticket_id: int) -> Optional[Ticket]:
        return next(
            (
                ticket
                for ticket in self._tickets
                if ticket.id == ticket_id
            ),
            None,
        )

    def resolve_ticket(self, ticket_id: int) -> bool:
        ticket = self.find_ticket(ticket_id)

        if ticket is None:
            return False

        ticket.status = "Resolved"
        return True

    def delete_ticket(self, ticket_id: int) -> bool:
        ticket = self.find_ticket(ticket_id)

        if ticket is None:
            return False

        self._tickets.remove(ticket)
        return True

    def get_tickets(self, query="all"):
        expression = QueryInterpreter.parse(query)

        matching_tickets = [
            ticket
            for ticket in self._tickets
            if expression.matches(ticket)
        ]

        return list(TicketIterator(matching_tickets))
