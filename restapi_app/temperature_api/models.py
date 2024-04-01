from django.db import models

class TemperatureReading(models.Model):
    city_id = models.IntegerField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
