from django.urls import path
from .views import SignupView, CustomLoginView, CustomLogoutView, BookingManageView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("", BookingManageView.as_view(), name="booking_list"),
]
