from rest_framework import generics
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from . import services

class ExpenseListCreateController(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return services.filter_expenses(self.request.query_params)

    def list(self, request, *args, **kwargs):
        queryset = services.filter_expenses(request.query_params)
        queryset = services.paginate_expenses(queryset, request.query_params)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ExpenseDetailController(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
