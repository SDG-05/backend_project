from django.db import models


class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048)
    code = models.CharField(max_length=10, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
