from django.db import models

class Tenant(models.Model):
  name = models.CharField(max_length=100)
  domain = models.CharField(max_length=50)
  config_json = models.JSONField()
  created_on = models.DateField(auto_now_add=True)