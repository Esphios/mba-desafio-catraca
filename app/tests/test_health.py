from django.db import connection
from django.test import SimpleTestCase, TransactionTestCase


class LivenessTests(SimpleTestCase):
    def test_TEST_A03_live_reports_process_running(self):
        response = self.client.get('/health/live')
        self.assertEqual(response.status_code, 200)


class ReadinessClosedTests(TransactionTestCase):
    def test_TEST_A03_ready_is_closed_before_bootstrap_and_worker(self):
        response = self.client.get('/health/ready')
        self.assertEqual(response.status_code, 503)


class DatabaseTests(TransactionTestCase):
    def test_TEST_A03_real_postgres_connection(self):
        self.assertEqual(connection.vendor, 'postgresql')
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            self.assertEqual(cursor.fetchone(), (1,))
