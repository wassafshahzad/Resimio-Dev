from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    """
    A form that extends Django's built-in UserCreationForm to include Bootstrap styling.
    """
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })

class LoginForm(AuthenticationForm):
    """
    A form that extends Django's built-in AuthenticationForm to include Bootstrap styling.
    """
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        for _, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })
