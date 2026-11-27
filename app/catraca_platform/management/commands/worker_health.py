from datetime import timedelta

from coredata.models import WorkerHeartbeat
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fail unless the worker loop has a recent database heartbeat.'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(seconds=5)
        if not WorkerHeartbeat.objects.filter(last_seen__gte=cutoff).exists():
            raise CommandError('Worker heartbeat is stale.')
        self.stdout.write('Worker heartbeat is fresh.')
