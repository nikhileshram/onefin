from django.db import models

# Create your models here.

class Movie(models.Model):

    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    genre = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.id