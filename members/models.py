from django.db import models

# Create your models here.
from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
