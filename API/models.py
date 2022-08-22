from django.db import models


class Summoner(models.Model):
    id = models.CharField(max_length=64)
    puuid = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
