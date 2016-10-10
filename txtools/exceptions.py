class TextXToolsError(Exception):
    """Base exception for textX tools."""


class ValidationError(TextXToolsError):
    """Used in model validation."""
