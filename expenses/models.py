from django.db import models
from categories.models import Category

class Expense(models.Model):
    # Connects to the Category model. If a category is deleted, its expenses are deleted too.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')

    # max_digits=10 means up to 99,999,999.99
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description or self.category.name} - {self.amount}"
