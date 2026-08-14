from django.urls import path
from .controllers import CategoryListCreateController, CategoryDetailController

urlpatterns = [
    path('categories/', CategoryListCreateController.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailController.as_view(), name='category-detail'),

]
