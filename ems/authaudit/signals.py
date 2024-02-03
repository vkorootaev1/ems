from django.contrib.auth import signals, get_user_model
from django.db import transaction
from authaudit.models import AuthAudit
from middlewares import get_current_request


def user_logged_in(sender, request, user, **kwargs):
    try:
        with transaction.atomic():
            AuthAudit.objects.create(
                type=AuthAudit.AUTH_CHOICES[0][0],
                username=user.username,
                user_pk=user.id,
                user_repr=user.__str__(),
                user=user,
                remote_ip=request.META['REMOTE_ADDR']
            )
    except Exception:
        pass


def user_logged_out(sender, request, user, **kwargs):
    try:
        with transaction.atomic():
            AuthAudit.objects.create(
                type=AuthAudit.AUTH_CHOICES[1][0],
                username=user.username,
                user_pk=user.id,
                user_repr=user.__str__(),
                user=user,
                remote_ip=request.META['REMOTE_ADDR']
            )
    except Exception:
        pass


def user_login_failed(sender, credentials, **kwargs):
    with transaction.atomic():
        user_model = get_user_model()
        request = get_current_request()
        print(reversed)
        AuthAudit.objects.create(
            type=AuthAudit.AUTH_CHOICES[2][0],
            username=credentials[user_model.USERNAME_FIELD],
            remote_ip=request.META['REMOTE_ADDR']
        )


signals.user_logged_in.connect(
    user_logged_in, dispatch_uid='auth_audit_signals_logged_in')
signals.user_logged_out.connect(
    user_logged_out, dispatch_uid='auth_audit_signals_logged_out')
signals.user_login_failed.connect(
    user_login_failed, dispatch_uid='auth_audit_signals_login_failed')
