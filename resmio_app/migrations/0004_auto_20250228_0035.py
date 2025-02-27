from django.db import migrations
from django.contrib.auth import get_user_model

def create_users(apps, schema_editor):
    User = get_user_model()

    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword',
        is_staff=True,
    )

    User.objects.create_user(
        username='regularuser',
        email='user@example.com',
        password='userpassword'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('resmio_app', '0003_alter_booking_date_alter_booking_status_and_more'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]
