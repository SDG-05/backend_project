from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Handles GET (list all) and POST (create new)
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Handles GET (details), PUT (update), and DELETE for a single book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
