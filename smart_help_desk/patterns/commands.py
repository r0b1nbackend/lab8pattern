# ==================================================
# COMMAND PATTERN
# ==================================================

class AddTicketCommand:
    def __init__(self, title, description, category):
        self.title = title.strip()
        self.description = description.strip()
        self.category = category

    def execute(self, mediator):
        return mediator.add_ticket(
            self.title,
            self.description,
            self.category,
        )


class ResolveTicketCommand:
    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id

    def execute(self, mediator):
        return mediator.resolve_ticket(self.ticket_id)


class DeleteTicketCommand:
    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id

    def execute(self, mediator):
        return mediator.delete_ticket(self.ticket_id)
