from typing import Optional


# ==================================================
# CHAIN OF RESPONSIBILITY PATTERN
# ==================================================

class ValidationHandler:
    def __init__(self):
        self._next: Optional["ValidationHandler"] = None

    def set_next(self, handler: "ValidationHandler"):
        self._next = handler
        return handler

    def handle(self, data: dict) -> Optional[str]:
        error = self.validate(data)

        if error:
            return error

        if self._next:
            return self._next.handle(data)

        return None

    def validate(self, data: dict) -> Optional[str]:
        return None


class TitleRequiredHandler(ValidationHandler):
    def validate(self, data: dict) -> Optional[str]:
        if not data.get("title", "").strip():
            return "Title is required."

        return None


class DescriptionLengthHandler(ValidationHandler):
    def validate(self, data: dict) -> Optional[str]:
        description = data.get("description", "").strip()

        if len(description) < 10:
            return (
                "Description must contain "
                "at least 10 characters."
            )

        return None


class CategoryHandler(ValidationHandler):
    ALLOWED_CATEGORIES = {"IT", "Account", "Other"}

    def validate(self, data: dict) -> Optional[str]:
        if data.get("category") not in self.ALLOWED_CATEGORIES:
            return "Please choose a valid category."

        return None


def build_validation_chain():
    title_handler = TitleRequiredHandler()
    description_handler = DescriptionLengthHandler()
    category_handler = CategoryHandler()

    title_handler.set_next(
        description_handler
    ).set_next(category_handler)

    return title_handler
