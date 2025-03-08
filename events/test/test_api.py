from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from events.models import Event
from datetime import date, time

class EventAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="test_user", password="test_user_password")
        
        # Get JWT token
        response = self.client.post("/api/auth/token/", {
            "username": "test_user",
            "password": "test_user_password"
        }, format="json")

        self.access_token = response.data["access"]
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}

        # Create a test event
        self.event = Event.objects.create(
            name="Django Workshop",
            description="Learn Django step by step",
            date=date(2025, 3, 10),
            time=time(14, 0),
            location="Online",
            max_capacity=100,
            created_by=self.user
        )

    def test_list_events(self):
        """Test retrieving all events"""
        response = self.client.get("/api/v1/events/", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  
        
    def test_get_single_event(self):
        """Test retrieving a single event by ID"""
        url = f"/api/v1/events/{self.event.id}/"
        response = self.client.get(url, **self.auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.event.id)
        self.assertEqual(response.data["name"], "Django Workshop")

    def test_get_non_existent_event(self):
        """Test retrieving an event that does not exist"""
        url = "/api/v1/events/9999/"  # Assuming this ID doesn't exist
        response = self.client.get(url, **self.auth_headers)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_create_event(self):
        """Test creating a new event"""
        data = {
            "name": "New Event",
            "description": "This is a test event",
            "date": "2025-04-15",
            "time": "16:00:00",
            "location": "Zoom",
            "max_capacity": 30
        }
        response = self.client.post("/api/v1/events/", data, format="json", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Event")

    def test_update_event(self):
        """Test updating an event"""
        update_data = {"name": "Updated Django Workshop"}
        url = f"/api/v1/events/{self.event.id}/"
        response = self.client.put(url, update_data, format="json", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Django Workshop")

    def test_delete_event(self):
        """Test deleting an event"""
        url = f"/api/v1/events/{self.event.id}/"
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_unauthorized_access(self):
        """Test accessing API without authentication"""
        response = self.client.get("/api/v1/events/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
