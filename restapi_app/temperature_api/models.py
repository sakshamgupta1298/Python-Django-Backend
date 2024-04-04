from django.db import models

class TemperatureReading(models.Model):
    id = models.AutoField(primary_key=True) 
    city_id = models.IntegerField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(unique=True)
    class Meta:
        db_table = 'temperature' 
