from django.db import models

# Create your models here.

class LogDescription(models.Model):
    title = models.CharField(max_length=255, unique=True)

class Log(models.Model):
    start = models.DateTimeField(db_index=True, null=False)
    end = models.DateTimeField(db_index=True, null=False)
    description = models.ForeignKey(LogDescription)
