from django.db import models


class AirlineModel(models.Model):
    oid = models.AutoField(primary_key=True)
    destination = models.CharField(max_length=30)
    destination_IATA = models.CharField(max_length=15)
    origin = models.CharField(max_length=30)
    origin_IATA = models.CharField(max_length=15)

    TICKET_CHOICES = (
        ("ONEWAY", "One-way"),
        ("RETURN", "Return"),
    )
    ticket = models.CharField(choices=TICKET_CHOICES, max_length=10, default="ONEWAY")

    departure = models.DateField()
    arrival = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ticket == "ONEWAY":
            self.arrival = None
        super().save(*args, **kwargs)
