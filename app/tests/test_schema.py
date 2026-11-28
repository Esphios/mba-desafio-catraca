import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier

from django.apps import apps
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError, close_old_connections, connection, transaction
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

    def test_TEST_A05_authorized_orm_writes_canonicalize_email(self):
        created = self.User.objects.create(
            email='  Case@Test.Example  ', name='Created', role='participant'
        )
        self.assertEqual(created.email, 'case@test.example')

        created.email = '  Saved@Test.Example  '
        created.save(update_fields=['email'])
        created.refresh_from_db()
        self.assertEqual(created.email, 'saved@test.example')

        self.User.objects.filter(pk=created.pk).update(email='  Updated@Test.Example  ')
        created.refresh_from_db()
        self.assertEqual(created.email, 'updated@test.example')

        bulk_created = self.User(email='  Bulk@Test.Example  ', name='Bulk', role='participant')
        self.User.objects.bulk_create([bulk_created])
        bulk_created.refresh_from_db()
        self.assertEqual(bulk_created.email, 'bulk@test.example')

        bulk_created.email = '  Bulk-Saved@Test.Example  '
        self.User.objects.bulk_update([bulk_created], ['email'])
        bulk_created.refresh_from_db()
        self.assertEqual(bulk_created.email, 'bulk-saved@test.example')

    def test_TEST_A05_bulk_email_writes_preserve_iterable_semantics(self):
        users = (
            self.User(email=email, name='Generated', role='participant')
            for email in (' Generated-A@Test.Example ', ' Generated-B@Test.Example ')
        )
        created = self.User.objects.bulk_create(users)
        self.assertEqual(
            sorted(user.email for user in created),
            ['generated-a@test.example', 'generated-b@test.example'],
        )

        for user in created:
            user.email = user.email.replace('generated-', ' Updated-').upper()
        self.User.objects.bulk_update((user for user in created), ['email'])
        self.assertEqual(
            sorted(
                self.User.objects.filter(pk__in=[user.pk for user in created]).values_list(
                    'email', flat=True
                )
            ),
            ['updated-a@test.example', 'updated-b@test.example'],
        )

    def test_TEST_A05_base_manager_bulk_create_canonicalizes_email(self):
        user = self.User(email=' Base-Create@Example.TEST ', name='Base', role='participant')

        self.User._base_manager.bulk_create([user])

        user.refresh_from_db()
        self.assertEqual(user.email, 'base-create@example.test')

    def test_TEST_A05_base_manager_update_canonicalizes_email(self):
        self.User._base_manager.filter(pk=self.participant.pk).update(
            email=' Base-Update@Example.TEST '
        )

        self.participant.refresh_from_db()
        self.assertEqual(self.participant.email, 'base-update@example.test')

    def test_TEST_A05_bulk_update_accepts_an_iterable_of_fields(self):
        self.participant.email = ' Iterator@Example.TEST '
        self.participant.name = 'Iterator'

        self.User.objects.bulk_update([self.participant], iter(('email', 'name')))

        self.participant.refresh_from_db()
        self.assertEqual(self.participant.email, 'iterator@example.test')
        self.assertEqual(self.participant.name, 'Iterator')

    def test_TEST_A05_deserialized_user_is_saved_with_canonical_email(self):
        payload = json.loads(serializers.serialize('json', [self.participant]))
        payload[0]['fields']['email'] = ' Deserialized@Example.TEST '

        for deserialized in serializers.deserialize('json', json.dumps(payload)):
            deserialized.save()

        self.participant.refresh_from_db()
        self.assertEqual(self.participant.email, 'deserialized@example.test')

    def test_TEST_A05_partial_save_only_normalizes_email_when_written(self):
        self.participant.email = 'invalid email'
        self.participant.name = 'Renamed'

        self.participant.save(update_fields=iter(('name',)))

        self.assertEqual(self.participant.email, 'invalid email')
        self.participant.refresh_from_db()
        self.assertEqual(self.participant.email, 'participant@example.test')
        self.assertEqual(self.participant.name, 'Renamed')

    def test_TEST_A05_email_casefold_expansion_and_canonical_length_are_enforced(self):
        expanded = self.User.objects.create(
            email='  Straße@Example.TEST  ', name='Unicode', role='participant'
        )
        self.assertEqual(expanded.email, 'strasse@example.test')

        expands_past_limit = 'a@' + ('ß.' * 84) + 'x'
        self.assertLess(len(expands_past_limit), 254)
        self.assertGreater(len(expands_past_limit.casefold()), 254)
        with self.assertRaises(ValidationError):
            self.User.objects.create(
                email=expands_past_limit, name='Too long after casefold', role='participant'
            )

    def test_TEST_A05_logical_email_duplicates_are_rejected(self):
        self.User.objects.create(email='  Logical@Test.Example  ', name='First', role='participant')
        self.assert_integrity_error(
            lambda: self.User.objects.create(
                email='logical@test.example', name='Duplicate', role='participant'
            )
        )

    def test_TEST_A05_concurrent_logical_email_duplicates_create_one_user(self):
        barrier = Barrier(2)

        def create_variant(email):
            close_old_connections()
            try:
                barrier.wait()
                with transaction.atomic():
                    self.User.objects.create(email=email, name='Concurrent', role='participant')
                return 'created'
            except IntegrityError:
                return 'duplicate'
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(
                    create_variant,
                    (' Concurrent@Test.Example ', 'concurrent@test.example'),
                )
            )

        self.assertCountEqual(results, ['created', 'duplicate'])
        self.assertEqual(
            self.User.objects.filter(email='concurrent@test.example').count(),
            1,
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
            cursor.execute(
                """
                SELECT pg_get_expr(index_catalog.indpred, index_catalog.indrelid)
                FROM pg_index AS index_catalog
                JOIN pg_class AS index_class ON index_class.oid = index_catalog.indexrelid
                JOIN pg_class AS table_class ON table_class.oid = index_catalog.indrelid
                WHERE table_class.relname = %s AND index_class.relname = %s
                """,
                [self.PaymentJob._meta.db_table, 'cd_job_queued_due_idx'],
            )
            queued_job_predicate = cursor.fetchone()[0]

        self.assertIn(('owner_id', 'id'), event_indexes)
        self.assertIn(('status', 'starts_at'), event_indexes)
        self.assertIn(('event_id', 'status'), ticket_indexes)
        self.assertIn(('participant_id', 'created_at'), ticket_indexes)
        self.assertIn(('due_at',), job_indexes)
        self.assertIsNotNone(queued_job_predicate)
        normalized_predicate = (
            queued_job_predicate.replace('(', '')
            .replace(')', '')
            .replace('::text', '')
            .replace('"', '')
            .replace(' ', '')
        )
        self.assertEqual(normalized_predicate, "state='queued'")
