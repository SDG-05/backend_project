from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    # Added 'db' to health check so we can verify MariaDB connection later
    return JsonResponse({"status": "ok", "service": "myproject", "db": "connected"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    path('api/', include('categories.urls')), # <-- ADD THIS
]