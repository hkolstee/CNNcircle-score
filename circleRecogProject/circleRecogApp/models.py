from django.db import models

# Create your models here.
class Circle(models.Model):
    circle = models.ImageField(upload_to = 'uploads/', height_field = None, width_field = None)
    score = models.FloatField()
    name = models.CharField(max_length=200)
    