from django.urls import path
from django.views.generic import RedirectView

from .views import (
    SignupView,
    CustomLoginView,
    CustomLogoutView,
    BookingManageView,
    BookingDeleteView,
    FacilityManageView,
    HealthCheckView,
)


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("", RedirectView.as_view(pattern_name="booking_list", permanent=False)),
    path("booking/", BookingManageView.as_view(), name="booking_list"),
    path(
        "booking/<uuid:booking_uuid>",
        BookingDeleteView.as_view(),
        name="booking_delete",
    ),
    path("facilities/", FacilityManageView.as_view(), name="facility_manage"),
    path("health_check/", HealthCheckView.as_view(), name="health_check"),
]
