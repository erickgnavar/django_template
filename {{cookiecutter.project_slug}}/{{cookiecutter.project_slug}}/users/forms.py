from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label=_("Confirm password"), widget=forms.PasswordInput, required=True
    )
    accept_terms = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "password",
            "confirm_password",
        )
        widgets = {
            "email": forms.EmailInput,
            "password": forms.PasswordInput,
        }

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(_("Password doesn't match"))
        return confirm_password


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)


class ResetPasswordForm(forms.Form):

    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput, required=True
    )
    confirm_password = forms.CharField(
        label=_("Confirm password"), widget=forms.PasswordInput, required=True
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(_("Password doesn't match"))
        return confirm_password
