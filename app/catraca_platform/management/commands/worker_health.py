from datetime import timedelta

from coredata.models import WorkerHeartbeat
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catraca_platform.clock import clock_now


class Command(BaseCommand):
    help = 'Fail unless the worker loop has a recent database heartbeat.'

    def handle(self, *args, **options):
        cutoff = clock_now() - timedelta(seconds=5)
        if not WorkerHeartbeat.objects.filter(
            worker_id=settings.CAT_WORKER_ID,
            last_seen__gte=cutoff,
        ).exists():
            raise CommandError('Worker heartbeat is stale.')
        self.stdout.write('Worker heartbeat is fresh.')
