# ==================================================
# ITERATOR PATTERN
# ==================================================

class TicketIterator:
    def __init__(self, tickets):
        self._tickets = list(tickets)
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._tickets):
            raise StopIteration

        ticket = self._tickets[self._index]
        self._index += 1

        return ticket
