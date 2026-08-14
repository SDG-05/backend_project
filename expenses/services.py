from .models import Expense

def filter_expenses(params):
    queryset = Expense.objects.all().select_related('category')

    category = params.get('category')
    if category:
        if category.isdigit():
            queryset = queryset.filter(category_id=category)
        else:
            queryset = queryset.filter(category__name__iexact=category)

    start_date = params.get('startDate')
    if start_date: queryset = queryset.filter(date__gte=start_date)

    end_date = params.get('endDate')
    if end_date: queryset = queryset.filter(date__lte=end_date)

    transaction_type = params.get('type')
    if transaction_type: queryset = queryset.filter(type=transaction_type)

    min_amount = params.get('minAmount')
    if min_amount: queryset = queryset.filter(amount__gte=min_amount)

    max_amount = params.get('maxAmount')
    if max_amount: queryset = queryset.filter(amount__lte=max_amount)

    sort = params.get('sort')
    if sort == 'date_desc': queryset = queryset.order_by('-date')
    elif sort == 'date_asc': queryset = queryset.order_by('date')
    elif sort == 'amount_desc': queryset = queryset.order_by('-amount')
    elif sort == 'amount_asc': queryset = queryset.order_by('amount')
    else: queryset = queryset.order_by('-created_at')

    return queryset

def paginate_expenses(queryset, params):
    try:
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 20))
        if page < 1: page = 1
        if limit < 1: limit = 20
        start = (page - 1) * limit
        end = start + limit
        return queryset[start:end]
    except ValueError:
        return queryset
