from rest_framework import generics
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        # Start with all expenses
        queryset = Expense.objects.all()
        params = self.request.query_params

        # 1. Filter by Category (supports name like 'food' or ID like '1')
        category = params.get('category')
        if category:
            if category.isdigit():
                queryset = queryset.filter(category_id=category)
            else:
                queryset = queryset.filter(category__name__iexact=category)

        # 2. Filter by Date Range
        start_date = params.get('startDate')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        end_date = params.get('endDate')
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # 3. Filter by Type (income/expense)
        type_ = params.get('type')
        if type_:
            queryset = queryset.filter(type=type_)

        # 4. Filter by Amount Range
        min_amount = params.get('minAmount')
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        max_amount = params.get('maxAmount')
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        # 5. Sorting
        sort = params.get('sort')
        if sort == 'date_desc':
            queryset = queryset.order_by('-date')
        elif sort == 'date_asc':
            queryset = queryset.order_by('date')
        elif sort == 'amount_desc':
            queryset = queryset.order_by('-amount')
        else:
            queryset = queryset.order_by('-created_at') # Default sort

        # 6. Pagination (page & limit)
        try:
            page = int(params.get('page', 1))
            limit = int(params.get('limit', 20))
            start = (page - 1) * limit
            end = start + limit
            return queryset[start:end]
        except ValueError:
            return queryset

# Handles GET (details), PUT (update), and DELETE for a single expense
class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
