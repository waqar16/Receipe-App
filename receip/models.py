from django.db import models
from django.contrib.auth.models import User


class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    receipe_name = models.CharField(max_length=300)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to='receipe-images')