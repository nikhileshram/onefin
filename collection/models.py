from django.db import models
from django.contrib.auth import get_user_model
from movie.models import Movie

# Create your models here.

class Collection(models.Model):

    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=1000, null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.id

# Create your models here.
class MovieCollection(models.Model):

    id = models.UUIDField(primary_key=True, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.id