from django.urls import path
from .controllers import ExpenseListCreateController, ExpenseDetailController

urlpatterns = [
    path('expenses/', ExpenseListCreateController.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailController.as_view(), name='expense-detail'),
]
