from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model


class UserRepository:
    """
    Repository class for handling user authentication-related database operations.
    """
    User = get_user_model()

    @classmethod
    def create_user(cls, username, email, password):
        """
        Creates a new user and returns it.
        """
        return cls.User.objects.create_user(username=username, email=email, password=password)

    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticates a user and returns the user object if valid.
        """
        return authenticate(username=username, password=password)

    @staticmethod
    def login_user(request, user):
        """
        Logs in the given user.
        """
        login(request, user)

    @staticmethod
    def logout_user(request):
        """
        Logs out the currently authenticated user.
        """
        logout(request)
