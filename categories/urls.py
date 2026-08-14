from django.urls import path
from .controllers import CategoryListCreateController

urlpatterns = [
    path('categories/', CategoryListCreateController.as_view(), name='category-list-create'),
]
