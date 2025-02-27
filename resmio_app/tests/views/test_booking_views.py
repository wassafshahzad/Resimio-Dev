from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from resmio_app.models import Booking, Facility

User = get_user_model()

class BookingManageViewTests(TestCase):
    """Tests for BookingManageView"""

    def setUp(self):
        """Set up a test user."""
        self.user = User.objects.create_user(username="testuser", password="password123", email="testuser@gmail.com")
        self.client.login(email="testuser@gmail.com", password="password123",)
        self.url = reverse("booking_list")

    @patch("resmio_app.repositories.booking_repository.BookingRepository.get_user_bookings")
    def test_booking_list_view(self, mock_get_user_bookings):
        """Test that the view lists user bookings."""
        mock_get_user_bookings.return_value = []
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        mock_get_user_bookings.assert_called_once_with(self.user)
        self.assertTemplateUsed(response, "booking/booking_manage.html")

    @patch("resmio_app.repositories.booking_repository.BookingRepository.is_facility_full")
    def test_booking_creation_fails_when_facility_is_full(self, mock_is_facility_full):
        """Test booking creation failure when facility is fully booked."""
        mock_is_facility_full.return_value = True

        facility = Facility(id=1, name="Gym", location="NY", capacity=10)
        data = {"facility": facility.id, "date": "2026-02-25"}
        response = self.client.post(self.url, data, follow=True)

        mock_is_facility_full.assert_called_once_with(facility)


    @patch("resmio_app.repositories.booking_repository.BookingRepository.create_booking")
    def test_booking_creation_raises_exception(self, mock_create_booking):
        """Test error handling when repository raises a ValueError."""
        mock_create_booking.side_effect = ValueError("Booking already exists.")

        facility = Facility(id=1, name="Gym", location="NY", capacity=10)
        data = {"facility": facility.id, "date": "2026-02-25"}

        _ = self.client.post(self.url, data, follow=True)

        mock_create_booking.assert_called_once()

class BookingDeleteViewTests(TestCase):
    """Tests for BookingDeleteView"""

    def setUp(self):
        """Set up a test user and booking."""
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@gmail.com")
        self.client.login(email="test@gmail.com", password="password123")
        self.booking = Booking.objects.create(
            user=self.user, 
            date="2025-02-25", 
            facility=Facility.objects.create(name="Gym", location="NY", capacity=10)
        )
        self.url = reverse("booking_delete", kwargs={"booking_uuid": self.booking.uuid})

    @patch("resmio_app.repositories.booking_repository.BookingRepository.delete_booking")
    def test_delete_booking_success(self, mock_delete_booking):
        """Test successful booking deletion."""
        mock_delete_booking.return_value = True

        _ = self.client.post(self.url, follow=True)

        mock_delete_booking.assert_called_once_with(self.booking.uuid, self.user)

    @patch("resmio_app.repositories.booking_repository.BookingRepository.delete_booking")
    def test_delete_booking_failure(self, mock_delete_booking):
        """Test failure when deletion is unsuccessful."""
        mock_delete_booking.return_value = False

        _ = self.client.post(self.url, follow=True)

        mock_delete_booking.assert_called_once_with(self.booking.uuid, self.user)
