from resmio_app.models import Booking, Facility
from datetime import date

class FacilityRepository:
    """
    Repository for handling database operations related to Facility.
    """

    @staticmethod
    def get_available_facilities():
        """
        Returns facilities that are NOT fully booked for today.
        """
        booked_facilities = Booking.objects.filter(date=date.today()).values_list("facility", flat=True)
        return Facility.objects.exclude(id__in=booked_facilities)

    @staticmethod
    def get_facility_by_id(facility_id):
        """
        Fetches a specific facility by ID.
        """
        return Facility.objects.filter(id=facility_id).first()

    @staticmethod
    def facility_exists(facility_id):
        """
        Checks if a facility exists by ID.
        """
        return Facility.objects.filter(id=facility_id).exists()
