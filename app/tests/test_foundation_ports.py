from datetime import UTC, datetime
from threading import Event as StopSignal
from types import ModuleType

from django.http import HttpResponse
from django.test import SimpleTestCase, TransactionTestCase, override_settings
from django.urls import include, path


def example_provider(actor, event_id):
    return actor, event_id


EXAMPLE_PARTIAL = 'tests/example_management_partial.html'


def example_operation(request):
    return HttpResponse('configured operation')


urlpatterns = [path('action/', example_operation)]


class ClockTests(SimpleTestCase):
    def test_TEST_A04_clock_now_returns_an_aware_utc_timestamp(self):
        from catraca_platform.clock import clock_now

        before = datetime.now(UTC)
        actual = clock_now()
        after = datetime.now(UTC)

        self.assertIs(actual.tzinfo, UTC)
        self.assertLessEqual(before, actual)
        self.assertLessEqual(actual, after)


class ManagementHooksTests(SimpleTestCase):
    def test_TEST_A04_default_operations_slot_and_urlconf_are_empty(self):
        from config.management_provider import (
            management_operations_patterns,
            management_partial,
        )

        self.assertIsNone(management_partial())
        self.assertEqual(management_operations_patterns(), [])

    @override_settings(
        MANAGEMENT_PROVIDER='tests.test_foundation_ports.example_provider',
        MANAGEMENT_PARTIAL='tests.test_foundation_ports.EXAMPLE_PARTIAL',
        MANAGEMENT_OPERATIONS_URLCONF='tests.test_foundation_ports',
    )
    def test_TEST_A04_management_hooks_resolve_configured_components(self):
        from config.management_provider import (
            management_operations_patterns,
            management_partial,
            management_snapshot,
        )

        self.assertEqual(management_snapshot('organizer', 'event-id'), ('organizer', 'event-id'))
        self.assertEqual(management_partial(), 'tests/example_management_partial.html')

        urlconf = ModuleType('configured_management_test')
        urlconf.urlpatterns = [path('gestao/eventos/', include(management_operations_patterns()))]
        with self.settings(ROOT_URLCONF=urlconf):
            response = self.client.get('/gestao/eventos/action/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'configured operation')


class FixtureFactoryTests(TransactionTestCase):
    def test_TEST_A05_fixture_factory_provides_isolated_scenarios_with_overrides(self):
        from tests.fixtures import fixture_factory

        owner = fixture_factory('organizer')
        other_owner = fixture_factory('organizer')
        attendee = fixture_factory('participant')
        event = fixture_factory('event', owner=owner, capacity=7)

        self.assertEqual((owner.role, attendee.role), ('organizer', 'participant'))
        self.assertNotEqual(owner.email, other_owner.email)
        event.refresh_from_db()
        self.assertEqual(event.owner_id, owner.pk)
        self.assertEqual(event.capacity, 7)


class WorkerPortTests(TransactionTestCase):
    def test_TEST_A01_worker_command_updates_heartbeat_and_stops_on_signal(self):
        from coredata.models import WorkerHeartbeat
        from worker.main import worker_command

        class StopAfterHeartbeat(StopSignal):
            def wait(self, timeout=None):
                self.set()
                return True

        stop = StopAfterHeartbeat()

        self.assertEqual(worker_command('test-worker', stop), 0)

        self.assertTrue(stop.is_set())
        self.assertTrue(WorkerHeartbeat.objects.filter(worker_id='test-worker').exists())
