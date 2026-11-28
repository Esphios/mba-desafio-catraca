from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def normalize_email(value: str) -> str:
    if not isinstance(value, str):
        raise ValidationError('Invalid email address.')
    canonical = value.strip().casefold()
    if not canonical or len(canonical) > 254:
        raise ValidationError('Invalid email address.')
    validate_email(canonical)
    return canonical
