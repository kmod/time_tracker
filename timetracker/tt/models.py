from django.db import models

# Create your models here.

class LogDescription(models.Model):
    title = models.CharField(max_length=255, unique=True)

class Log(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    description = models.ForeignKey(LogDescription)
