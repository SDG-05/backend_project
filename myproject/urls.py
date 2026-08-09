from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "service": "myproject", "db": "connected"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    path('api/', include('categories.urls')),
    path('api/', include('expenses.urls')),
    path('api/', include('books.urls')), # new
    path('api/authors/', include('authors.urls')),
]
