import secrets
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import CITextField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from .managers import UserManager


class User(PermissionsMixin, TimeStampedModel, AbstractBaseUser):
    email = CITextField(verbose_name=_("Email address"), max_length=255, unique=True,)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    name = models.CharField(_("Name"), max_length=100, null=True)

    email_confirmation_token = models.CharField(
        max_length=64, default=secrets.token_hex, null=True
    )
    email_confirmation_datetime = models.DateTimeField(
        _("Email confirmation date"), editable=False, null=True
    )

    reset_password_token = models.CharField(max_length=64, null=True, editable=False)
    reset_password_token_expiration_date = models.DateTimeField(
        null=True, editable=False
    )

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def confirm_account(self):
        self.is_active = True
        self.email_confirmation_token = None
        self.email_confirmation_datetime = timezone.now()
        self.save()

    def gen_reset_password_token(self):
        self.reset_password_token = secrets.token_hex()
        self.reset_password_token_expiration_date = timezone.now() + timedelta(hours=24)
        self.save()

    def reset_password(self, password):
        self.set_password(password)
        self.reset_password_token = None
        self.reset_password_token_expiration_date = None
        self.save()
