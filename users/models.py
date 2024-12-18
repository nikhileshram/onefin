from django.db import models

# Create your models here.

class User(models.Model):

    id = models.UUIDField(primary_key=True, editable=False)
    user_name = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=1000, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.id
