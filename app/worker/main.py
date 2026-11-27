import os
import signal
import time

import django
from django.db import close_old_connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from coredata.models import WorkerHeartbeat

STOP_REQUESTED = False


def request_stop(signum, frame):
    del signum, frame
    global STOP_REQUESTED
    STOP_REQUESTED = True


def run():
    worker_id = os.environ.get('CAT_WORKER_ID', 'worker-1')
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    while not STOP_REQUESTED:
        close_old_connections()
        WorkerHeartbeat.objects.update_or_create(worker_id=worker_id)
        time.sleep(1)
    close_old_connections()
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
