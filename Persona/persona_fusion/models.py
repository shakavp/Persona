from django.db import models


class Persona(models.Model):
    name = models.CharField(max_length=100, editable=False, unique=True)
    level = models.IntegerField(editable=False)
    arcana = models.CharField(max_length=100, editable=False)
    price = models.IntegerField(editable=False)
    special = models.BooleanField()
