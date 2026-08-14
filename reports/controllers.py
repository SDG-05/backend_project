from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Budget
from .serializers import BudgetSerializer
from . import services

class MonthlyReportController(APIView):
    def get(self, request):
        return Response(services.get_monthly_report(request.query_params.get('year')), status=status.HTTP_200_OK)

class YearlyReportController(APIView):
    def get(self, request):
        return Response(services.get_yearly_report(), status=status.HTTP_200_OK)

class ByCategoryReportController(APIView):
    def get(self, request):
        return Response(services.get_by_category_report(request.query_params.get('startDate'), request.query_params.get('endDate')), status=status.HTTP_200_OK)

class BudgetStatusController(APIView):
    def get(self, request):
        month, year = request.query_params.get('month'), request.query_params.get('year')
        if not month or not year:
            return Response({"error": "Both 'month' and 'year' query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            month, year = int(month), int(year)
        except ValueError:
            return Response({"error": "'month' and 'year' must be integers."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(services.get_budget_status(month, year), status=status.HTTP_200_OK)

class BudgetListCreateController(generics.ListCreateAPIView):
    queryset = Budget.objects.all().select_related('category')
    serializer_class = BudgetSerializer

class BudgetDetailController(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all().select_related('category')
    serializer_class = BudgetSerializer
