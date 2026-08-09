from django.shortcuts import render

import string
import random

from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortURL
from .serializers import ShortURLSerializer


def generate_code(length=6):
    characters = string.ascii_letters + string.digits

    while True:
        code = ''.join(random.choices(characters, k=length))

        if not ShortURL.objects.filter(code=code).exists():
            return code


class ShortenURLView(APIView):

    def post(self, request):
        original_url = request.data.get('url')

        if not original_url:
            return Response(
                {'error': 'URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        code = generate_code()

        short_url = ShortURL.objects.create(
            original_url=original_url,
            code=code
        )

        return Response(
            {
                'original_url': short_url.original_url,
                'short_url': f'http://127.0.0.1:8000/s/{code}',
                'code': code
            },
            status=status.HTTP_201_CREATED
        )


class RedirectURLView(APIView):

    def get(self, request, code):

        short_url = get_object_or_404(
            ShortURL,
            code=code
        )

        short_url.clicks += 1
        short_url.save(update_fields=['clicks'])

        return redirect(short_url.original_url)