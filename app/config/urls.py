from django.http import HttpResponse
from django.urls import path


def live(request):
    return HttpResponse('live', content_type='text/plain')


def ready(request):
    # Bootstrap and worker health are delivered in subsequent F01 tasks.
    return HttpResponse('not ready', status=503, content_type='text/plain')


urlpatterns = [path('health/live', live), path('health/ready', ready)]
