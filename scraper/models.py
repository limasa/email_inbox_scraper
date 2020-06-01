from django.db import models


class Email_Data(models.Model):
    portal = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True)
    reference = models.CharField(max_length=250, null=True)
    message = models.CharField(max_length=1000, null=True)
    name = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=20, null=True)
    price = models.CharField(max_length=20, null=True)
