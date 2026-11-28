import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

ROLE_NAME = 'catraca_runtime'
SAFE_IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
RUNTIME_DML_TABLES = (
    'accounts_user',
    'accounts_user_groups',
    'accounts_user_user_permissions',
    'coredata_event',
    'coredata_paymentjob',
    'coredata_ticket',
    'coredata_workerheartbeat',
    'django_session',
)


class Command(BaseCommand):
    help = 'Create the runtime role and grant DML-only access after migrations.'

    def handle(self, *args, **options):
        password = os.environ.get('CAT_RUNTIME_DB_PASSWORD')
        database_name = settings.DATABASES['default']['NAME']
        if not password:
            raise CommandError('CAT_RUNTIME_DB_PASSWORD is required.')
        if not SAFE_IDENTIFIER.fullmatch(database_name):
            raise CommandError('Unsafe database name.')

        quoted_database = connection.ops.quote_name(database_name)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'catraca_runtime') THEN
                        CREATE ROLE catraca_runtime LOGIN;
                    END IF;
                END
                $$;
                """
            )
            cursor.execute('ALTER ROLE catraca_runtime PASSWORD %s', [password])
            cursor.execute(
                'ALTER ROLE catraca_runtime NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT'
            )
            cursor.execute('REVOKE CREATE ON SCHEMA public FROM PUBLIC')
            cursor.execute(f'GRANT CONNECT ON DATABASE {quoted_database} TO {ROLE_NAME}')
            cursor.execute(f'GRANT USAGE ON SCHEMA public TO {ROLE_NAME}')
            cursor.execute(f'GRANT SELECT ON ALL TABLES IN SCHEMA public TO {ROLE_NAME}')
            cursor.execute(
                f'REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public FROM {ROLE_NAME}'
            )
            for table_name in RUNTIME_DML_TABLES:
                quoted_table = connection.ops.quote_name(table_name)
                cursor.execute(
                    f'GRANT INSERT, UPDATE, DELETE ON TABLE {quoted_table} TO {ROLE_NAME}'
                )

        self.stdout.write('Runtime database role ready with DML-only grants.')
