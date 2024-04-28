from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Username"}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "placeholder": "Password"}
        ),
    )


class RegistrationForm(UserCreationForm):
    """
    Form for customer registration.
    """

    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"placeholder": "Your Name"})
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Your Name"}),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Password"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Confirm Password"}
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(f"Дана пошта вже зареєстрована")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Паролі не співпадають")

        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "password1", "password2")
