from django.db import models


class Server(models.Model):
    hostname = models.CharField(max_length=50)
    ip = models. CharField(max_length=32)
