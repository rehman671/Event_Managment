from django.db import models

from user.models import CustomUser

# Create your models here.


class EventModel(models.Model):
    eid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=50)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="owner")
    attendees = models.ManyToManyField(CustomUser, related_name="attendees", default=None)

    def __str__(self):
        return self.title
