from django.db import models

# Create your models here.
class Circle(models.Model):
    name = models.CharField(max_length = 200)
    circularity = models.IntegerField()
    circle = models.ImageField(upload_to='circles/')