from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "HEAD"])
def healthz(_request):
    return HttpResponse("ok", content_type="text/plain")
