from datetime import timedelta
from uuid import uuid4

from accounts.models import User
from catraca_platform.clock import clock_now
from coredata.models import Event
from django.db import transaction


@transaction.atomic
def fixture_factory(scenario, **overrides):
    """Persist an isolated synthetic organizer, participant, or event for tests."""
    if scenario in ('organizer', 'participant'):
        values = {
            'email': f'{scenario}-{uuid4().hex}@example.test',
            'name': scenario.title(),
            'role': scenario,
        }
        return User.objects.create_user(**(values | overrides))

    if scenario == 'event':
        values = {
            'name': 'Synthetic event',
            'venue': 'Test venue',
            'starts_at': clock_now() + timedelta(days=1),
            'capacity': 10,
            'price_cents': 1000,
        } | overrides
        if 'owner' not in values and 'owner_id' not in values:
            values['owner'] = fixture_factory('organizer')
        return Event.objects.create(**values)

    raise ValueError(f'Unknown fixture scenario: {scenario}')
