from django.db import models
from categories.models import Category

class Expense(models.Model):
    # Add choices for Income vs Expense
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='expense') # <-- NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description or self.category.name} - {self.amount}"
