import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

SEED_IDENTITIES = (
    {
        'email': 'gestao.a@example.test',
        'name': 'Organizador A',
        'role': 'organizer',
        'password': 'LocalA-2026!',
    },
    {
        'email': 'gestao.b@example.test',
        'name': 'Organizador B',
        'role': 'organizer',
        'password': 'LocalB-2026!',
    },
    {
        'email': 'pessoa@example.test',
        'name': 'Participante',
        'role': 'participant',
        'password': 'LocalP-2026!',
    },
)


class Command(BaseCommand):
    help = 'Create the fixed synthetic identities for demo and test profiles.'

    def handle(self, *args, **options):
        profile = os.environ.get('CAT_PROFILE', 'demo')
        if profile not in {'demo', 'test'}:
            raise CommandError('Seed is allowed only in demo or test profiles.')

        User = get_user_model()
        created_count = 0
        with transaction.atomic():
            for identity in SEED_IDENTITIES:
                existing = User.objects.filter(email=identity['email']).first()
                if existing:
                    if existing.role != identity['role'] or existing.name != identity['name']:
                        raise CommandError(
                            f'Seed identity collision for {identity["email"]}; existing account '
                            'was not modified.'
                        )
                    continue
                User.objects.create_user(**identity)
                created_count += 1

        self.stdout.write(
            f'Seed ready: {len(SEED_IDENTITIES)} identities ({created_count} created).'
        )
