from resmio_app.models import Booking
from datetime import date
from django.db import IntegrityError

class BookingRepository:
    """
    Repository for handling database operations related to Booking.
    """

    @staticmethod
    def get_user_bookings(user):
        """
        Retrieves all bookings for a given user.
        """
        return Booking.objects.filter(user=user)

    @staticmethod
    def create_booking(user, facility, booking_date):
        """
        Creates a booking for a facility with the following validations.
        """

        if booking_date < date.today():
            raise ValueError("Cannot book a facility in the past.")

        if Booking.objects.filter(user=user, facility=facility, date=booking_date).exists():
            raise ValueError("You have already booked this facility on this date.")

        try:
            return Booking.objects.create(user=user, facility=facility, date=booking_date)
        except IntegrityError:
            raise ValueError("Error creating the booking. Please try again.")

    @staticmethod
    def delete_booking(booking_id, user):
        """
        Deletes a user's booking if it exists.
        """
        booking = Booking.objects.filter(id=booking_id, user=user).first()
        if booking:
            booking.delete()
            return True
        return False

    @staticmethod
    def is_facility_full(facility):
        """
        Checks if a facility is at full capacity.
        """
        return Booking.objects.filter(facility=facility, date=date.today()).count() >= facility.capacity
