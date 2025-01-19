from django.db import models

# Create your models here.
class Task(models.Model):
    text = models.CharField(max_length=2000)
    completed = models.BooleanField(default=False)
    date = models.DateField()

    def __str__(self):
        return self.text
