from django.urls import path

from .views import ShortenURLView, RedirectURLView


urlpatterns = [
    path(
        'shorten/',
        ShortenURLView.as_view(),
        name='shorten-url'
    ),

    path(
        's/<str:code>/',
        RedirectURLView.as_view(),
        name='redirect-url'
    ),
]