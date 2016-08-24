from django.db import models


class Participant(models.Model):
    last_test = models.CharField(max_length=255)
    session = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    gender = models.BooleanField()
    allow_info_usage = models.BooleanField()
    directory = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=1000)

