from django.db import models

# Create your models here.
class Resid(models.Model):
    resid = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.resid)