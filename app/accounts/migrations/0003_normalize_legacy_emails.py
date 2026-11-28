from django.core.exceptions import ValidationError
from django.db import migrations

from accounts.email_policy import normalize_email


def normalize_legacy_emails(apps, schema_editor):
    user = apps.get_model('accounts', 'User')
    users = user._base_manager.using(schema_editor.connection.alias)
    table = schema_editor.quote_name(user._meta.db_table)
    # Prevent writes between validating the full set of addresses and updating it.
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f'LOCK TABLE {table} IN SHARE ROW EXCLUSIVE MODE')

    seen = set()
    changes = []
    for pk, email in users.values_list('pk', 'email').iterator():
        try:
            canonical = normalize_email(email)
        except ValidationError:
            raise RuntimeError('Legacy account email migration found an invalid address.') from None
        if canonical in seen:
            raise RuntimeError('Legacy account email migration found colliding addresses.')
        seen.add(canonical)
        if email != canonical:
            changes.append((pk, canonical))

    for pk, canonical in changes:
        users.filter(pk=pk).update(email=canonical)


class Migration(migrations.Migration):
    dependencies = [('accounts', '0002_enforce_canonical_email')]
    operations = [migrations.RunPython(normalize_legacy_emails, migrations.RunPython.noop)]
