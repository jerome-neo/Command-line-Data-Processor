from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError


class OutputValidator(Validator):
    def validate(self, document: Document) -> None:
        if document.text not in {"csv", "parquet", "xlsx", "y", "n", "yes", "no", "gz", "bz2", "xz"}:
            raise ValidationError(message="Invalid command")
