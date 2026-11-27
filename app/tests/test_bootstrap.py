import os
from datetime import timedelta
from unittest.mock import patch

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TransactionTestCase
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
