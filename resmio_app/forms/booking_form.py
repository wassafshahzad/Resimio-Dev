from django import forms
from django.utils import timezone

from resmio_app.models import Booking
from resmio_app.repositories import FacilityRepository, BookingRepository

class BookingForm(forms.ModelForm):
    """
    Booking form that ensures
    """

    class Meta:
        model   = Booking
        fields  = ["facility", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        available_facilities = FacilityRepository.get_available_facilities()
        self.fields["facility"].queryset = available_facilities

    def clean_date(self):
        """ Ensure the booking date is valid. """
        booking_date = self.cleaned_data.get("date")

        if booking_date < timezone.now():
            raise forms.ValidationError("You cannot book a past date.")

        return booking_date

    def clean(self):
        """ Ensure no duplicate bookings for the same user on the same day. """
        cleaned_data = super().clean()
        facility = cleaned_data.get("facility")
        booking_date = cleaned_data.get("date")

        if facility and booking_date:
            if BookingRepository.get_user_bookings(self.user).filter(facility=facility, date=booking_date).exists():
                raise forms.ValidationError("You have already booked this facility on this date.")

        return cleaned_data
