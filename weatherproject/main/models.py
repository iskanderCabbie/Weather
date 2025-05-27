from django.db import models

class CitySearch(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.session_key})"
