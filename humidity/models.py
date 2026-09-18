# humidity/models.py
from django.db import models

class JejuWeather(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    nx = models.IntegerField()
    ny = models.IntegerField()

    class Meta:
        db_table = 'weather_jejuweather'
        managed = False  # 기존 테이블을 활용

    def __str__(self):
        return self.name