import os
import signal
from threading import Event

import django
from django.conf import settings
from django.db import close_old_connections


def worker_command(worker_id: str, stop: Event) -> int:
    from coredata.models import WorkerHeartbeat

    try:
        while not stop.is_set():
            close_old_connections()
            WorkerHeartbeat.objects.update_or_create(worker_id=worker_id)
            stop.wait(1)
    finally:
        close_old_connections()
    return 0


def main() -> int:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    stop = Event()

    def request_stop(_signum, _frame):
        stop.set()

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    return worker_command(settings.CAT_WORKER_ID, stop)


if __name__ == '__main__':
    raise SystemExit(main())
