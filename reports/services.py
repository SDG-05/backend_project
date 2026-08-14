from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from expenses.models import Expense
from .models import Budget

def get_monthly_report(year=None):
    expenses = Expense.objects.all()
    if year: expenses = expenses.filter(date__year=year)

    expense_data = expenses.filter(type='expense').annotate(month=TruncMonth('date')).values('month').annotate(total_expense=Sum('amount')).order_by('month')
    income_data = expenses.filter(type='income').annotate(month=TruncMonth('date')).values('month').annotate(total_income=Sum('amount')).order_by('month')

    expense_dict = {item['month'].strftime('%Y-%m'): float(item['total_expense'] or 0) for item in expense_data}
    income_dict = {item['month'].strftime('%Y-%m'): float(item['total_income'] or 0) for item in income_data}
    all_months = sorted(set(list(expense_dict.keys()) + list(income_dict.keys())))

    return [{'month': m, 'total_income': income_dict.get(m, 0), 'total_expense': expense_dict.get(m, 0), 'net_balance': income_dict.get(m, 0) - expense_dict.get(m, 0)} for m in all_months]

def get_yearly_report():
    expense_data = Expense.objects.filter(type='expense').annotate(year=TruncYear('date')).values('year').annotate(total_expense=Sum('amount')).order_by('year')
    income_data = Expense.objects.filter(type='income').annotate(year=TruncYear('date')).values('year').annotate(total_income=Sum('amount')).order_by('year')

    expense_dict = {item['year'].year: float(item['total_expense'] or 0) for item in expense_data}
    income_dict = {item['year'].year: float(item['total_income'] or 0) for item in income_data}
    all_years = sorted(set(list(expense_dict.keys()) + list(income_dict.keys())))

    return [{'year': y, 'total_income': income_dict.get(y, 0), 'total_expense': expense_dict.get(y, 0), 'net_balance': income_dict.get(y, 0) - expense_dict.get(y, 0)} for y in all_years]

def get_by_category_report(start_date=None, end_date=None):
    expenses = Expense.objects.filter(type='expense')
    if start_date: expenses = expenses.filter(date__gte=start_date)
    if end_date: expenses = expenses.filter(date__lte=end_date)
    return {item['category__name']: float(item['total'] or 0) for item in expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')}

def get_budget_status(month, year):
    budgets = Budget.objects.filter(month=month, year=year).select_related('category')
    results = []
    for budget in budgets:
        actual_spending = Expense.objects.filter(category=budget.category, type='expense', date__month=month, date__year=year).aggregate(total=Sum('amount'))['total'] or 0
        remaining = budget.amount - actual_spending
        percentage_used = (actual_spending / budget.amount * 100) if budget.amount > 0 else 0
        results.append({
            'category': budget.category.name, 'budget_limit': float(budget.amount), 'actual_spending': float(actual_spending),
            'remaining': float(remaining), 'percentage_used': round(float(percentage_used), 2),
            'status': 'over_budget' if remaining < 0 else 'within_budget',
        })
    return results
