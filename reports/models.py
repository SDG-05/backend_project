from django.db import models
from categories.models import Category


class Budget(models.Model):
    """
    Stores the monthly budget limit for each category.
    Example: Food category gets 5000 per month.
    """
    MONTHS = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Budget limit for this category")
    month = models.PositiveSmallIntegerField(choices=MONTHS)
    year = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate budgets for same category/month/year
        unique_together = ['category', 'month', 'year']

    def __str__(self):
        return f"{self.category.name} - {self.get_month_display()} {self.year}: {self.amount}"
