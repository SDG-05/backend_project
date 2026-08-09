from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer
from books.models import Book
from books.serializers import BookSerializer

# 1. GET /api/authors/ and POST /api/authors/
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# 2. GET, PUT, PATCH, DELETE /api/authors/<id>/
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# 3. GET /api/authors/<id>/books/ (The special endpoint)
class AuthorBooksView(APIView):
    def get(self, request, pk):
        # Find all books where the author ID matches the URL ID
        books = Book.objects.filter(author_id=pk)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
