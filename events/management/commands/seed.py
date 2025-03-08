from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from events.models import Event
from django.db import connection
from datetime import date, time

class Command(BaseCommand):
    help = "Seeds the database with sample events"

    def handle(self, *args, **kwargs):
        # Ensure a test user exists
        user, created = User.objects.get_or_create(username="test_user")

        if created:
            user.set_password("test_user_password")
            user.save()

        # Clear existing data
        Event.objects.all().delete()

        # Reset ID sequence
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='events_event';")

        self.stdout.write(self.style.WARNING("Deleted existing events and reset ID counter."))

        # Sample event data
        event_data = [
            {"name": "Django Workshop", "description": "Learn Django basics", "date": "2025-03-10", "time": "14:00:00", "location": "Online", "max_capacity": 100},
            {"name": "Python Meetup", "description": "Networking for Python enthusiasts", "date": "2025-04-05", "time": "18:00:00", "location": "New York", "max_capacity": 50},
            {"name": "AI Conference", "description": "Discussing AI trends", "date": "2025-05-20", "time": "09:00:00", "location": "San Francisco", "max_capacity": 200},
            {"name": "React Workshop", "description": "Learn React fundamentals", "date": "2025-06-15", "time": "16:00:00", "location": "Online", "max_capacity": 80},
            {"name": "Cybersecurity Seminar", "description": "Best practices for security", "date": "2025-07-25", "time": "10:30:00", "location": "London", "max_capacity": 120},
        ]

        # Create events
        events = [Event(**data, created_by=user) for data in event_data]
        Event.objects.bulk_create(events)

        self.stdout.write(self.style.SUCCESS("Successfully seeded database with events!"))
