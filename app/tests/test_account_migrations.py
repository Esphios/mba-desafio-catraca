from accounts.models import User
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.test import TransactionTestCase


class CanonicalEmailUpgradeTests(TransactionTestCase):
    initial = ('accounts', '0001_initial')

    def setUp(self):
        executor = MigrationExecutor(connection)
        self.latest = executor.loader.graph.leaf_nodes()
        executor.migrate([self.initial])
        historical = executor.loader.project_state([self.initial]).apps.get_model(
            'accounts', 'User'
        )
        self.old_users = historical._base_manager

    def tearDown(self):
        self.old_users.all().delete()
        MigrationExecutor(connection).migrate(self.latest)

    def legacy_user(self, email):
        return self.old_users.create(email=email, name='Legacy', role='participant')

    def test_TEST_A05_upgrade_canonicalizes_legacy_account_without_replacing_it(self):
        legacy = self.legacy_user('  Legacy@Example.TEST  ')

        MigrationExecutor(connection).migrate(self.latest)

        user = User.objects.get(pk=legacy.pk)
        self.assertEqual(user.email, 'legacy@example.test')
        self.assertEqual(user.role, 'participant')
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create(email=' Legacy@EXAMPLE.TEST ', name='Duplicate', role='participant')

    def assert_upgrade_rejected_without_changes(self, reason, expected):
        with self.assertRaisesRegex(RuntimeError, reason) as failure:
            MigrationExecutor(connection).migrate(self.latest)

        self.assertEqual(
            dict(self.old_users.values_list('pk', 'email')),
            {user.pk: user.email for user in expected},
        )
        migrations = MigrationRecorder(connection).applied_migrations()
        self.assertNotIn(('accounts', '0003_normalize_legacy_emails'), migrations)
        self.assertNotIn('@', str(failure.exception))

    def test_TEST_A05_upgrade_aborts_atomically_on_canonical_email_collision(self):
        unrelated = self.legacy_user(' Unrelated@Example.TEST ')
        first = self.legacy_user('  Duplicate@Example.TEST  ')
        second = self.legacy_user('duplicate@example.test')

        self.assert_upgrade_rejected_without_changes(
            'colliding addresses', [unrelated, first, second]
        )

    def test_TEST_A05_upgrade_aborts_atomically_on_invalid_legacy_email(self):
        unrelated = self.legacy_user(' Unrelated@Example.TEST ')
        invalid = self.legacy_user('invalid legacy address')

        self.assert_upgrade_rejected_without_changes('invalid address', [unrelated, invalid])
