from datetime import timedelta

from catraca_platform.clock import clock_now
from coredata.models import WorkerHeartbeat
from django.conf import settings
from django.db import DatabaseError, connection
from django.db.migrations.exceptions import InconsistentMigrationHistory
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse
from django.urls import path


def live(request):
    return HttpResponse('live', content_type='text/plain')


def ready(request):
    try:
        executor = MigrationExecutor(connection)
        executor.loader.check_consistent_history(connection)
        targets = executor.loader.graph.leaf_nodes()
        if executor.migration_plan(targets):
            return HttpResponse('migrations pending', status=503, content_type='text/plain')
        cutoff = clock_now() - timedelta(seconds=5)
        if not WorkerHeartbeat.objects.filter(
            worker_id=settings.CAT_WORKER_ID,
            last_seen__gte=cutoff,
        ).exists():
            return HttpResponse('worker heartbeat stale', status=503, content_type='text/plain')
    except InconsistentMigrationHistory:
        return HttpResponse('migration history inconsistent', status=503, content_type='text/plain')
    except DatabaseError:
        return HttpResponse('database unavailable', status=503, content_type='text/plain')
    return HttpResponse('ready', content_type='text/plain')


urlpatterns = [path('health/live', live), path('health/ready', ready)]
