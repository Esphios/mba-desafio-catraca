import uuid
from datetime import timedelta

from django.apps import apps
from django.db import DataError, IntegrityError, connection, transaction
from django.test import SimpleTestCase, TransactionTestCase
from django.utils import timezone

MAX_CAPACITY = 2**31 - 1
MAX_PRICE_CENTS = 2**53 - 1


class SchemaInstallationTests(SimpleTestCase):
    def test_TEST_A05_custom_user_and_business_models_are_installed(self):
        self.assertTrue(apps.is_installed('accounts'))
        self.assertTrue(apps.is_installed('coredata'))
        self.assertEqual(
            apps.get_model('accounts', 'User')._meta.pk.get_internal_type(), 'UUIDField'
        )


class SchemaIntegrityTests(TransactionTestCase):
    def setUp(self):
        self.User = apps.get_model('accounts', 'User')
        self.Event = apps.get_model('coredata', 'Event')
        self.Ticket = apps.get_model('coredata', 'Ticket')
        self.PaymentJob = apps.get_model('coredata', 'PaymentJob')
        self.WorkerHeartbeat = apps.get_model('coredata', 'WorkerHeartbeat')
        self.owner = self.User.objects.create_user(
            email='owner@example.test',
            name='Owner',
            role='organizer',
            password='not-a-real-secret',
        )
        self.participant = self.User.objects.create_user(
            email='participant@example.test',
            name='Participant',
            role='participant',
            password='not-a-real-secret',
        )
        self.event = self.Event.objects.create(
            owner=self.owner,
            name='Schema event',
            venue='Test venue',
            starts_at=timezone.now() + timedelta(days=1),
            capacity=10,
            price_cents=10_000,
        )

    def assert_integrity_error(self, factory):
        with self.assertRaises((DataError, IntegrityError)), transaction.atomic():
            factory()

    def ticket_values(self, **overrides):
        values = {
            'event': self.event,
            'code': uuid.uuid4().hex[:12].upper(),
            'channel': 'web',
            'participant': self.participant,
            'buyer_email': self.participant.email,
            'price_cents': self.event.price_cents,
            'status': 'pending',
        }
        values.update(overrides)
        return values

    def job_values(self, ticket, **overrides):
        values = {
            'ticket': ticket,
            'outcome': 'approved',
            'due_at': timezone.now() + timedelta(seconds=3),
            'state': 'queued',
            'processed_at': None,
        }
        values.update(overrides)
        return values

    def test_TEST_A05_valid_graph_and_ticket_without_job_persist(self):
        ticket_without_job = self.Ticket.objects.create(**self.ticket_values())
        partner_ticket = self.Ticket.objects.create(
            **self.ticket_values(
                code='PARTNER00001',
                channel='partner',
                participant=None,
                buyer_email='partner@example.test',
            )
        )
        job = self.PaymentJob.objects.create(**self.job_values(partner_ticket))
        heartbeat = self.WorkerHeartbeat.objects.create(worker_id='worker-1')

        self.assertFalse(self.PaymentJob.objects.filter(ticket=ticket_without_job).exists())
        self.assertEqual(job.ticket_id, partner_ticket.id)
        self.assertEqual(heartbeat.worker_id, 'worker-1')

    def test_TEST_A05_user_email_and_role_constraints_reject_invalid_rows(self):
        self.assert_integrity_error(
            lambda: self.User.objects.create_user(
                email=self.owner.email,
                name='Duplicate',
                role='organizer',
                password='not-a-real-secret',
            )
        )
        self.assert_integrity_error(
            lambda: self.User.objects.create(
                email='bad-role@example.test', name='Bad role', role='administrator'
            )
        )

    def test_TEST_A05_event_constraints_reject_fk_status_and_numeric_limits(self):
        invalid_values = (
            {'owner_id': uuid.uuid4()},
            {'status': 'deleted'},
            {'capacity': 0},
            {'capacity': MAX_CAPACITY + 1},
            {'price_cents': 0},
            {'price_cents': MAX_PRICE_CENTS + 1},
        )
        for values in invalid_values:
            with self.subTest(values=values):
                defaults = {
                    'owner': self.owner,
                    'name': 'Invalid event',
                    'venue': 'Test venue',
                    'starts_at': timezone.now() + timedelta(days=2),
                    'capacity': 1,
                    'price_cents': 1,
                }
                defaults.update(values)
                self.assert_integrity_error(
                    lambda defaults=defaults: self.Event.objects.create(**defaults)
                )

    def test_TEST_A05_ticket_code_constraint_and_uniqueness_are_database_enforced(self):
        self.Ticket.objects.create(**self.ticket_values(code='ABCDEF123456'))
        for code in ('SHORT123456', 'TOOLONG1234567', 'abcdef123456', 'INVALID-1234'):
            with self.subTest(code=code):
                self.assert_integrity_error(
                    lambda code=code: self.Ticket.objects.create(**self.ticket_values(code=code))
                )
        self.assert_integrity_error(
            lambda: self.Ticket.objects.create(**self.ticket_values(code='ABCDEF123456'))
        )

    def test_TEST_A05_ticket_constraints_reject_fk_status_channel_price_and_mixed_buyer(self):
        invalid_values = (
            {'event_id': uuid.uuid4()},
            {'participant_id': uuid.uuid4()},
            {'status': 'expired'},
            {'channel': 'box_office'},
            {'price_cents': 0},
            {'price_cents': MAX_PRICE_CENTS + 1},
            {'channel': 'web', 'participant': None},
            {'channel': 'partner', 'participant': self.participant},
        )
        for values in invalid_values:
            with self.subTest(values=values):
                self.assert_integrity_error(
                    lambda values=values: self.Ticket.objects.create(**self.ticket_values(**values))
                )

    def test_TEST_A05_payment_job_constraints_reject_duplicate_invalid_state_and_outcome(self):
        ticket = self.Ticket.objects.create(**self.ticket_values())
        self.PaymentJob.objects.create(**self.job_values(ticket))
        self.assert_integrity_error(
            lambda: self.PaymentJob.objects.create(**self.job_values(ticket))
        )

        invalid_values = (
            {'outcome': 'unknown'},
            {'state': 'processing'},
            {'state': 'queued', 'processed_at': timezone.now()},
            {'state': 'done', 'processed_at': None},
            {'state': 'ignored', 'processed_at': None},
        )
        for values in invalid_values:
            with self.subTest(values=values):
                fresh_ticket = self.Ticket.objects.create(**self.ticket_values())
                self.assert_integrity_error(
                    lambda values=values, fresh_ticket=fresh_ticket: self.PaymentJob.objects.create(
                        **self.job_values(fresh_ticket, **values)
                    )
                )

    def test_TEST_A05_required_query_indexes_exist(self):
        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(
                cursor, self.Event._meta.db_table
            )
            event_indexes = {
                tuple(details['columns']) for details in constraints.values() if details['index']
            }
            constraints = connection.introspection.get_constraints(
                cursor, self.Ticket._meta.db_table
            )
            ticket_indexes = {
                tuple(details['columns']) for details in constraints.values() if details['index']
            }
            constraints = connection.introspection.get_constraints(
                cursor, self.PaymentJob._meta.db_table
            )
            job_indexes = {
                tuple(details['columns']) for details in constraints.values() if details['index']
            }

        self.assertIn(('owner_id', 'id'), event_indexes)
        self.assertIn(('status', 'starts_at'), event_indexes)
        self.assertIn(('event_id', 'status'), ticket_indexes)
        self.assertIn(('participant_id', 'created_at'), ticket_indexes)
        self.assertIn(('due_at',), job_indexes)
