from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.urls import path
from django.views.static import serve

from app.views import EncryptedJsonREST


def ensure_authenticated(request: HttpRequest):
    if not request.user.is_authenticated:
        raise PermissionDenied()


def protected_serve(request, **kwargs):
    ensure_authenticated(request)
    return serve(request, **kwargs)


urlpatterns = []

if settings.API_ENABLED:
    urlpatterns.append(
        path('api/json/<str:org>/<uuid:uuid>', EncryptedJsonREST.as_view()))
