from celery.utils.log import get_task_logger
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _

from config.celery import app
from {{cookiecutter.project_slug}}.common.utils import Email

from .models import User


logger = get_task_logger(__name__)


@app.task(
    name="users.send_confirmation_email",
    retry_limit=3,
    default_retry_delay=10,
    bind=True,
)
def send_confirmation_email(self, user_id):
    logger.info("Email confirmation for user:%d", user_id)
    try:
        user = User.objects.get(id=user_id)
        assert not user.is_active, f"The user {user.email} is already active"
        path = reverse(
            "users:confirm-email", kwargs={"token": user.email_confirmation_token},
        )
        return Email.send_mail(
            template_name="email/confirm-email.html",
            context={"user": user, "confirm_link": f"{settings.DOMAIN}{path}"},
            subject=_("Confirmation email"),
            to=[user.email],
        )
    except Exception as ex:
        self.retry(exc=ex)
    logger.info("New user %d confirmation email notification sent", user.id)


@app.task(
    name="users.send_reset_password_email",
    retry_limit=3,
    default_retry_delay=10,
    bind=True,
)
def send_reset_password_email(self, user_id):
    logger.info("Reset password email message for user:%d", user_id)
    try:
        user = User.objects.get(id=user_id)
        assert user.is_active, f"The user {user.email} is not active"
        path = reverse(
            "users:reset-password", kwargs={"token": user.reset_password_token}
        )
        return Email.send_mail(
            template_name="email/reset-password.html",
            context={"user": user, "reset_link": f"{settings.DOMAIN}{path}"},
            subject=_("Reset password link"),
            to=[user.email],
        )
    except Exception as ex:
        self.retry(exc=ex)
    logger.info("Reset password email for %d was sent", user.id)
