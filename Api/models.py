from django.db import models

# Create your models here.

class ExampleModel(models.Model):
    app_label = 'Api'
    name = models.CharField(max_length=100)
    description = models.TextField()
