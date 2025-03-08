from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField()
    joined_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
