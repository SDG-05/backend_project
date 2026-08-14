from django.urls import path
from .controllers import (
    MonthlyReportController,
    YearlyReportController,
    ByCategoryReportController,
    BudgetStatusController,
    BudgetListCreateController,
)

urlpatterns = [
    path('reports/monthly/', MonthlyReportController.as_view(), name='report-monthly'),
    path('reports/yearly/', YearlyReportController.as_view(), name='report-yearly'),
    path('reports/by-category/', ByCategoryReportController.as_view(), name='report-by-category'),
    path('reports/budget-status/', BudgetStatusController.as_view(), name='report-budget-status'),
    path('reports/budgets/', BudgetListCreateController.as_view(), name='budget-list-create'),
]
