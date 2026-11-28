from django.conf import settings
from django.urls import include, path
from django.utils.module_loading import import_string


def management_snapshot(actor, event_id):
    provider = import_string(settings.MANAGEMENT_PROVIDER)
    return provider(actor, event_id)


def management_partial():
    dotted_path = settings.MANAGEMENT_PARTIAL
    return import_string(dotted_path) if dotted_path else None


def management_operations_patterns():
    urlconf = settings.MANAGEMENT_OPERATIONS_URLCONF
    return [path('', include(urlconf))] if urlconf else []
