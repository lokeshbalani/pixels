from django.db import models

# Create your models here.
class Image(models.Model):
    description = models.CharField(max_length=255, blank=True)
    image = models.FileField(upload_to='image/')
    uploaded_at = models.DateTimeField(auto_now_add=True)