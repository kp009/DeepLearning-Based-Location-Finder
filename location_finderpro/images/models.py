from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    
    def __str__(self):
        return self.image.name
