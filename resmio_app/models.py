import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """
    Abstract base model to automatically assign a UUID before saving.

    Attributes:
        id (int): Auto-incrementing primary key.
        uuid (UUID): A unique identifier for each instance.
        created_at (DateTime): Timestamp when the instance was created.
        updated_at (DateTime): Timestamp when the instance was last updated.
    """
    
    id         = models.AutoField(primary_key=True)
    uuid       = models.UUIDField(unique=True, editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Automatically assigns a UUID before saving if it's not set."""

        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        email (str): The user's email address (used for authentication).
        phone_number (str): Optional phone number field.
        is_verified (bool): Indicates whether the user's email is verified.
    """

    email       = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Facility(BaseModel):
    """
    Model representing a facility.

    Attributes:
        name (str): The name of the facility (must be unique).
        location (str): The physical address or location details of the facility.
        capacity (int): The maximum number of people the facility can accommodate.
    """
    name     = models.CharField(max_length=255, unique=True, db_index=True)
    location = models.CharField(max_length=500, db_index=True)
    capacity = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["location"])
        ]


    def __str__(self):
        return self.name


class Booking(BaseModel):
    """
    Model representing a booking for a facility.

    Attributes:
        user (User): The user who made the booking.
        facility (Facility): The facility being booked.
        date (DateTime): The date and time of the booking.
        status (str): The current status of the booking (e.g., pending, confirmed, canceled).
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    facility = models.ForeignKey('Facility', on_delete=models.CASCADE, related_name="bookings")
    date     = models.DateTimeField(db_index=True)
    status   = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)

    def __str__(self):
        return f"{self.user.username} - {self.facility.name} ({self.date})"
    class Meta:
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["facility", "date"])
        ]