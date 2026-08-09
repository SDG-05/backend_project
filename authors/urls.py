from django.urls import path
from .views import AuthorListCreateView, AuthorDetailView, AuthorBooksView

urlpatterns = [
    path('', AuthorListCreateView.as_view(), name='author-list'),
    path('<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('<int:pk>/books/', AuthorBooksView.as_view(), name='author-books'),
]
