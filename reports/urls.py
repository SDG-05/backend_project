from django.urls import path
from .views import (
    MonthlyReportView,
    YearlyReportView,
    ByCategoryReportView,
    BudgetStatusView,
    BudgetListCreateView,
)

urlpatterns = [
    path('reports/monthly/', MonthlyReportView.as_view(), name='report-monthly'),
    path('reports/yearly/', YearlyReportView.as_view(), name='report-yearly'),
    path('reports/by-category/', ByCategoryReportView.as_view(), name='report-by-category'),
    path('reports/budget-status/', BudgetStatusView.as_view(), name='report-budget-status'),
    path('reports/budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
]
