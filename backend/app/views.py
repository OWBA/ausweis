from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.static import serve

from app.models import Member


class EncryptedJsonREST(View):
    http_method_names = ['get']

    def get(self, request: HttpRequest, *args, **kwargs):
        return serveStaticJson(request, **kwargs)
        # return serveDynamicJson(**kwargs)


def memberOr404(kwargs: 'dict[str, str]'):
    org, uuid = kwargs['org'], kwargs['uuid']
    return get_object_or_404(Member, uuid=uuid, organization__slug=org)


def serveStaticJson(request: HttpRequest, **kwargs):
    org, uuid = kwargs['org'], kwargs['uuid']
    return serve(
        request, path=f'{org}/{uuid}', document_root=settings.EXPORT_PATH)


def serveDynamicJson(**kwargs):
    mem = memberOr404(kwargs)
    return HttpResponse(
        mem.json_encrypted, content_type='application/octet-stream')
