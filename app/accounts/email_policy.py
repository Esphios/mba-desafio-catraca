from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models


def normalize_email(value: str) -> str:
    if not isinstance(value, str):
        raise ValidationError('Invalid email address.')
    canonical = value.strip().casefold()
    if not canonical or len(canonical) > 254:
        raise ValidationError('Invalid email address.')
    validate_email(canonical)
    return canonical


class CanonicalEmailField(models.EmailField):
    def pre_save(self, model_instance, add):
        canonical = normalize_email(super().pre_save(model_instance, add))
        setattr(model_instance, self.attname, canonical)
        return canonical

    def get_db_prep_save(self, value, connection):
        # Django fixture loading skips pre_save and writes literal values directly.
        # bulk_update builds SQL expressions from emails already normalized by the manager.
        if not hasattr(value, 'as_sql'):
            value = normalize_email(value)
        return super().get_db_prep_save(value, connection)
