from models import Ticket


# ==================================================
# INTERPRETER PATTERN
# ==================================================

class QueryExpression:
    def matches(self, ticket: Ticket) -> bool:
        raise NotImplementedError


class AllExpression(QueryExpression):
    def matches(self, ticket: Ticket) -> bool:
        return True


class StatusExpression(QueryExpression):
    def __init__(self, status: str):
        self.status = status

    def matches(self, ticket: Ticket) -> bool:
        return ticket.status.lower() == self.status.lower()


class CategoryExpression(QueryExpression):
    def __init__(self, category: str):
        self.category = category

    def matches(self, ticket: Ticket) -> bool:
        return ticket.category.lower() == self.category.lower()


class AndExpression(QueryExpression):
    def __init__(self, expressions):
        self.expressions = expressions

    def matches(self, ticket: Ticket) -> bool:
        return all(
            expression.matches(ticket)
            for expression in self.expressions
        )


class QueryInterpreter:
    ALLOWED_STATUSES = {"open", "resolved"}
    ALLOWED_CATEGORIES = {"it", "account", "other"}

    @classmethod
    def parse(cls, query: str) -> QueryExpression:
        query = (query or "").strip()

        if not query or query.lower() == "all":
            return AllExpression()

        expressions = []

        for token in query.split():
            if ":" not in token:
                raise ValueError(
                    f"Invalid filter: {token}. "
                    "Use status:open or category:IT."
                )

            key, value = token.split(":", 1)
            key = key.lower()
            value = value.strip()

            if (
                key == "status"
                and value.lower() in cls.ALLOWED_STATUSES
            ):
                expressions.append(StatusExpression(value))

            elif (
                key == "category"
                and value.lower() in cls.ALLOWED_CATEGORIES
            ):
                categories = {
                    "it": "IT",
                    "account": "Account",
                    "other": "Other",
                }

                expressions.append(
                    CategoryExpression(categories[value.lower()])
                )

            else:
                raise ValueError(
                    f"Invalid filter: {token}. "
                    "Check the status or category value."
                )

        return AndExpression(expressions)
