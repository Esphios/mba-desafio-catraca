import os
from datetime import timedelta
from unittest.mock import patch

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.test import TransactionTestCase, override_settings
from django.utils import timezone


class BootstrapSeedTests(TransactionTestCase):
    def test_TEST_A01_seed_demo_creates_exact_idempotent_hashed_identities(self):
        User = apps.get_model('accounts', 'User')
        unrelated = User.objects.create_user(
            email='unrelated@example.test',
            name='Unrelated',
            role='participant',
            password='Unrelated-2026!',
        )
        original_password = unrelated.password

        with patch.dict(os.environ, {'CAT_PROFILE': 'demo'}):
            call_command('seed_demo')
            first_ids = dict(User.objects.exclude(pk=unrelated.pk).values_list('email', 'id'))
            call_command('seed_demo')

        self.assertEqual(
            set(first_ids),
            {
                'gestao.a@example.test',
                'gestao.b@example.test',
                'pessoa@example.test',
            },
        )
        self.assertEqual(
            dict(User.objects.exclude(pk=unrelated.pk).values_list('email', 'id')),
            first_ids,
        )
        self.assertEqual(User.objects.filter(role='organizer').count(), 2)
        self.assertEqual(User.objects.filter(role='participant').count(), 2)
        self.assertEqual(User.objects.get(pk=unrelated.pk).password, original_password)
        self.assertTrue(
            User.objects.get(email='gestao.a@example.test').check_password('LocalA-2026!')
        )
        self.assertNotEqual(
            User.objects.get(email='gestao.a@example.test').password,
            'LocalA-2026!',
        )

    def test_TEST_A01_seed_demo_rejects_non_demo_or_test_profile(self):
        with (
            patch.dict(os.environ, {'CAT_PROFILE': 'release'}),
            self.assertRaisesRegex(CommandError, 'demo or test'),
        ):
            call_command('seed_demo')


class ReadinessTests(TransactionTestCase):
    def test_TEST_A01_ready_requires_a_fresh_worker_database_heartbeat(self):
        WorkerHeartbeat = apps.get_model('coredata', 'WorkerHeartbeat')

        self.assertEqual(self.client.get('/health/ready').status_code, 503)
        heartbeat = WorkerHeartbeat.objects.create(worker_id='worker-1')
        self.assertEqual(self.client.get('/health/ready').status_code, 200)
        WorkerHeartbeat.objects.filter(pk=heartbeat.pk).update(
            last_seen=timezone.now() - timedelta(seconds=6)
        )
        self.assertEqual(self.client.get('/health/ready').status_code, 503)

    @override_settings(CAT_WORKER_ID='worker-1')
    def test_TEST_A01_ready_ignores_fresh_heartbeat_from_another_worker(self):
        WorkerHeartbeat = apps.get_model('coredata', 'WorkerHeartbeat')
        expected = WorkerHeartbeat.objects.create(worker_id='worker-1')
        WorkerHeartbeat.objects.filter(pk=expected.pk).update(
            last_seen=timezone.now() - timedelta(seconds=6)
        )
        WorkerHeartbeat.objects.create(worker_id='rogue-worker')

        self.assertEqual(self.client.get('/health/ready').status_code, 503)

        WorkerHeartbeat.objects.filter(pk=expected.pk).update(last_seen=timezone.now())
        self.assertEqual(self.client.get('/health/ready').status_code, 200)

    @override_settings(CAT_WORKER_ID='worker-1')
    def test_TEST_A01_worker_health_ignores_fresh_heartbeat_from_another_worker(self):
        WorkerHeartbeat = apps.get_model('coredata', 'WorkerHeartbeat')
        expected = WorkerHeartbeat.objects.create(worker_id='worker-1')
        WorkerHeartbeat.objects.filter(pk=expected.pk).update(
            last_seen=timezone.now() - timedelta(seconds=6)
        )
        WorkerHeartbeat.objects.create(worker_id='rogue-worker')

        with self.assertRaisesRegex(CommandError, 'stale'):
            call_command('worker_health')

        WorkerHeartbeat.objects.filter(pk=expected.pk).update(last_seen=timezone.now())
        call_command('worker_health')

    def test_TEST_A01_ready_rejects_inconsistent_migration_history(self):
        WorkerHeartbeat = apps.get_model('coredata', 'WorkerHeartbeat')
        WorkerHeartbeat.objects.create(worker_id='worker-1')
        recorder = MigrationRecorder(connection)
        recorder.record_unapplied('auth', '0001_initial')

        try:
            self.assertEqual(self.client.get('/health/ready').status_code, 503)
            self.assertFalse(recorder.migration_qs.filter(app='auth', name='0001_initial').exists())
        finally:
            recorder.record_applied('auth', '0001_initial')

        self.assertEqual(self.client.get('/health/ready').status_code, 200)

    def test_TEST_A01_ready_rejects_pending_migration_without_applying_it(self):
        WorkerHeartbeat = apps.get_model('coredata', 'WorkerHeartbeat')
        WorkerHeartbeat.objects.create(worker_id='worker-1')
        recorder = MigrationRecorder(connection)
        recorder.record_unapplied('sessions', '0001_initial')

        try:
            self.assertEqual(self.client.get('/health/ready').status_code, 503)
            self.assertFalse(
                recorder.migration_qs.filter(app='sessions', name='0001_initial').exists()
            )
        finally:
            recorder.record_applied('sessions', '0001_initial')

        self.assertEqual(self.client.get('/health/ready').status_code, 200)
