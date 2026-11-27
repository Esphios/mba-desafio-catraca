from datetime import timedelta

from coredata.models import WorkerHeartbeat
from django.db import DatabaseError, connection
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone


def live(request):
    return HttpResponse('live', content_type='text/plain')


def ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1 FROM django_migrations LIMIT 1')
            cursor.fetchone()
        cutoff = timezone.now() - timedelta(seconds=5)
        if not WorkerHeartbeat.objects.filter(last_seen__gte=cutoff).exists():
            return HttpResponse('worker heartbeat stale', status=503, content_type='text/plain')
    except DatabaseError:
        return HttpResponse('database unavailable', status=503, content_type='text/plain')
    return HttpResponse('ready', content_type='text/plain')


urlpatterns = [path('health/live', live), path('health/ready', ready)]
