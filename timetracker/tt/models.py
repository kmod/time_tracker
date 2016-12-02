from django.db import models

# Create your models here.

class LogDescription(models.Model):
    title = models.CharField(max_length=255, unique=True)

class Log(models.Model):
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    description = models.ForeignKey(LogDescription)
