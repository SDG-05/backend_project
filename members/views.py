from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Member
from .serializers import MemberSerializer

# 1. GET /api/members/ (List) and POST /api/members/ (Create)
class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

# 2. GET, PATCH, PUT, DELETE /api/members/<id>/
class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
