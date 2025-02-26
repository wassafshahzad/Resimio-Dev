from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms.authentication_forms import SignUpForm, LoginForm
from .repositories.user_repository import UserRepository

class SignupView(FormView):
    """
    Handles user signup using Django's FormView and UserRepository.
    """
    template_name = "auth/signup.html"
    form_class    = SignUpForm
    success_url   = reverse_lazy("home")

    def form_valid(self, form):
        user = UserRepository.create_user(
            username = form.cleaned_data["username"],
            email    = form.cleaned_data["email"],
            password = form.cleaned_data["password1"]
        )
        UserRepository.login_user(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    """
    Handles user login using Django's built-in LoginView.
    """
    template_name               = "auth/login.html"
    form_class                  = LoginForm
    redirect_authenticated_user = True
    success_url                 = reverse_lazy("home")

class CustomLogoutView(LogoutView):
    """
    Handles user logout using Django's built-in LogoutView.
    """
    next_page = reverse_lazy("login")
