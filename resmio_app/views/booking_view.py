from django.views.generic import ListView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from resmio_app.models import Booking
from resmio_app.forms import BookingForm
from resmio_app.repositories import BookingRepository

class BookingManageView(LoginRequiredMixin, ListView, FormView):
    """
    Displays a list of user's bookings and provides a form to create new bookings.
    """
    model               = Booking
    template_name       = "booking/booking_manage.html"
    context_object_name = "bookings"
    form_class          = BookingForm
    success_url         = reverse_lazy("booking_list")
    login_url           = reverse_lazy("login")
    object_list         = []

    def get_queryset(self):
        """ Fetches all bookings for the logged-in user. """
        return BookingRepository.get_user_bookings(self.request.user)

    def get_form_kwargs(self):
        """ Passes the user to the form for filtering available facilities. """
        kwargs         = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """ Handles booking creation with validation checks. """
        facility     = form.cleaned_data["facility"]
        booking_date = form.cleaned_data["date"]
        if BookingRepository.is_facility_full(facility):
            messages.error(self.request, f"'{facility.name}' is fully booked.")
            return self.form_invalid(form)

        try:
            BookingRepository.create_booking(self.request.user, facility, booking_date)
            messages.success(self.request, "Booking successfully created.")
            return super().form_valid(form)
        except ValueError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allows users to delete their bookings.
    """
    model         = Booking
    success_url   = reverse_lazy("booking_list")
    template_name = "bookings/booking_confirm_delete.html"

    def post(self,*args, **kwargs):
        booking_uuid = kwargs["booking_uuid"]
        if BookingRepository.delete_booking(booking_uuid, self.request.user):
            messages.success(self.request, "Booking canceled successfully.")
        else:
            messages.error(self.request, "Unable to cancel booking.")
        return redirect(self.success_url)
