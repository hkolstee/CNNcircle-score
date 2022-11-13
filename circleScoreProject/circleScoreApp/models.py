from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Circle(models.Model):
    artist_name = models.CharField(max_length = 200)
    circularity = models.DecimalField(max_digits = 11, decimal_places=10)
    circle = models.ImageField(upload_to='circles/')
    draw_date = models.DateTimeField(auto_now_add = True)
    
    # when accessed in the API
    def __str__(self):
        return ("[Circularity: " + str(self.circularity) + "]\n" +
                "[Drawn by: " + self.artist_name + "]\n" +
                "Draw date: " + str(self.draw_date) + "\n")

    # custom method to see if drawn today (for now 24 hours before)
    def wasDrawnToday(self):
        return self.draw_date >= timezone.now() - datetime.timedelta(days=1)

    # to also delete the local file override the delete function
    def delete(self, using=None, keep_parents=False):
        self.circle.delete()
        super().delete()