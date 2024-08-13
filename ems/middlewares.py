from threading import local
from auditlog.context import set_actor
from auditlog.middleware import AuditlogMiddleware as _AuditlogMiddleware
from django.utils.functional import SimpleLazyObject


class AuditlogMiddleware(_AuditlogMiddleware):

    def __call__(self, request):
        remote_addr = self._get_remote_addr(request)

        user = SimpleLazyObject(lambda: getattr(request, "user", None))

        context = set_actor(actor=user, remote_addr=remote_addr)

        with context:
            return self.get_response(request)


_thread_locals = local()


def get_current_request():
    return getattr(_thread_locals, 'request', None)


class AuthAuditMiddleware:

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):

        _thread_locals.request = request
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        _thread_locals.request = request
        return None
