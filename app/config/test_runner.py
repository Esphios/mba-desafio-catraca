from django.test.runner import DiscoverRunner


class NonEmptyRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        if not suite.countTestCases():
            raise RuntimeError('No tests discovered')
        return super().run_suite(suite, **kwargs)

    def suite_result(self, suite, result, **kwargs):
        return super().suite_result(suite, result, **kwargs) + len(result.skipped)
