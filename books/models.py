from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", blank=True)
    published_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

