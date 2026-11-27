from unittest import TestResult, TestSuite

from config.test_runner import NonEmptyRunner
from django.test import SimpleTestCase


class RunnerTests(SimpleTestCase):
    def test_TEST_A03_empty_suite_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, 'No tests'):
            NonEmptyRunner().run_suite(TestSuite())

    def test_TEST_A03_skipped_test_fails_closed(self):
        result = TestResult()
        result.addSkip(self, 'unavailable')
        self.assertNotEqual(NonEmptyRunner().suite_result(TestSuite(), result), 0)
