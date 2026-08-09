from django.db.models import Sum, Q, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from expenses.models import Expense
from .models import Budget
from .serializers import BudgetSerializer


class MonthlyReportView(APIView):
    """
    GET /api/reports/monthly?year=2026
    Returns monthly breakdown of income and expenses for a given year.
    """
    def get(self, request):
        year = request.query_params.get('year')

        expenses = Expense.objects.all()
        if year:
            expenses = expenses.filter(date__year=year)

        # Group by month, calculate total expenses
        expense_data = (
            expenses.filter(type='expense')
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_expense=Sum('amount'))
            .order_by('month')
        )

        # Group by month, calculate total income
        income_data = (
            expenses.filter(type='income')
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_income=Sum('amount'))
            .order_by('month')
        )

        # Merge into a single response
        expense_dict = {item['month'].strftime('%Y-%m'): float(item['total_expense']) for item in expense_data}
        income_dict = {item['month'].strftime('%Y-%m'): float(item['total_income']) for item in income_data}

        # Get all months that appear in either
        all_months = sorted(set(list(expense_dict.keys()) + list(income_dict.keys())))

        results = []
        for month in all_months:
            exp = expense_dict.get(month, 0)
            inc = income_dict.get(month, 0)
            results.append({
                'month': month,
                'total_income': inc,
                'total_expense': exp,
                'net_balance': inc - exp,
            })

        return Response(results, status=status.HTTP_200_OK)


class YearlyReportView(APIView):
    """
    GET /api/reports/yearly
    Returns yearly breakdown of income and expenses.
    """
    def get(self, request):
        # Group by year, calculate total expenses
        expense_data = (
            Expense.objects.filter(type='expense')
            .annotate(year=TruncYear('date'))
            .values('year')
            .annotate(total_expense=Sum('amount'))
            .order_by('year')
        )

        # Group by year, calculate total income
        income_data = (
            Expense.objects.filter(type='income')
            .annotate(year=TruncYear('date'))
            .values('year')
            .annotate(total_income=Sum('amount'))
            .order_by('year')
        )

        expense_dict = {item['year'].year: float(item['total_expense']) for item in expense_data}
        income_dict = {item['year'].year: float(item['total_income']) for item in income_data}

        all_years = sorted(set(list(expense_dict.keys()) + list(income_dict.keys())))

        results = []
        for year in all_years:
            exp = expense_dict.get(year, 0)
            inc = income_dict.get(year, 0)
            results.append({
                'year': year,
                'total_income': inc,
                'total_expense': exp,
                'net_balance': inc - exp,
            })

        return Response(results, status=status.HTTP_200_OK)


class ByCategoryReportView(APIView):
    """
    GET /api/reports/by-category?startDate=2026-01-01&endDate=2026-12-31
    Returns total spending grouped by category.
    Example response: {"Food": 4500, "Transport": 1200}
    """
    def get(self, request):
        expenses = Expense.objects.filter(type='expense')

        # Optional date range filter
        start_date = request.query_params.get('startDate')
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        end_date = request.query_params.get('endDate')
        if end_date:
            expenses = expenses.filter(date__lte=end_date)

        # Group by category name, sum the amounts
        category_totals = (
            expenses
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        # Format as {"CategoryName": amount}
        results = {item['category__name']: float(item['total']) for item in category_totals}

        return Response(results, status=status.HTTP_200_OK)


class BudgetStatusView(APIView):
    """
    GET /api/reports/budget-status?month=8&year=2026
    Compares actual spending against budget limits for each category.
    """
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response(
                {"error": "Both 'month' and 'year' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {"error": "'month' and 'year' must be integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all budgets for this month/year
        budgets = Budget.objects.filter(month=month, year=year).select_related('category')

        results = []
        for budget in budgets:
            # Calculate actual spending for this category in this month
            actual_spending = (
                Expense.objects.filter(
                    category=budget.category,
                    type='expense',
                    date__month=month,
                    date__year=year
                ).aggregate(total=Sum('amount'))['total'] or 0
            )

            remaining = budget.amount - actual_spending
            percentage_used = (actual_spending / budget.amount * 100) if budget.amount > 0 else 0

            results.append({
                'category': budget.category.name,
                'budget_limit': float(budget.amount),
                'actual_spending': float(actual_spending),
                'remaining': float(remaining),
                'percentage_used': round(float(percentage_used), 2),
                'status': 'over_budget' if remaining < 0 else 'within_budget',
            })

        return Response(results, status=status.HTTP_200_OK)


class BudgetListCreateView(APIView):
    """
    GET /api/reports/budgets/ - List all budgets
    POST /api/reports/budgets/ - Create a new budget
    """
    def get(self, request):
        budgets = Budget.objects.all().select_related('category')
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
