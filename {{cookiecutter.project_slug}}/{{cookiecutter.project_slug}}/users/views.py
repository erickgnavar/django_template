from datetime import timedelta

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import generic


from . import forms, tasks
from .models import User


class SignupView(generic.CreateView):

    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        tasks.send_confirmation_email.delay(self.object.id)
        messages.success(
            self.request,
            _(
                "A confirmation email was sent, please follow the instructions to complete your registration."
            ),
        )
        return response


class ConfirmEmailView(generic.RedirectView):
    def get_redirect_url(self, **kwargs):
        token = kwargs.get("token")
        success_message = _(
            "Your email address was confirmed, please login to access your account"
        )
        try:
            user = User.objects.get(email_confirmation_token=token, is_active=False)
            user.confirm_account()
            messages.success(self.request, success_message)
        except User.DoesNotExist:
            pass

        return reverse("pages:home")


class ForgotPasswordView(generic.FormView):

    template_name = "users/forgot-password.html"
    form_class = forms.ForgotPasswordForm
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        message = _(
            "If you entered a valid email address a link will be sent to this address to reset your password"
        )
        try:
            user = User.objects.get(email=email, is_active=True)
            user.gen_reset_password_token()
            tasks.send_reset_password_email.delay(user.id)
        except User.DoesNotExist:
            # we don't care about an email that doesn't exist
            pass
        messages.success(self.request, message)
        return super().form_valid(form)


class ResetPasswordView(generic.FormView):

    success_url = reverse_lazy("pages:home")
    form_class = forms.ResetPasswordForm
    template_name = "users/reset-password.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(
            User,
            reset_password_token=kwargs.get("token"),
            reset_password_token_expiration_date__lt=timezone.now()
            + timedelta(hours=24),
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.user.reset_password(form.cleaned_data.get("password"))
        return super().form_valid(form)
