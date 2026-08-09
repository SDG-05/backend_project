from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def health_check(request):
    return JsonResponse({"status": "ok", "service": "myproject"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    
    # Core Apps
    path('api/', include('categories.urls')),
    path('api/', include('expenses.urls')),
    path('api/', include('books.urls')),
    path('api/', include('reports.urls')),
    path('api/', include('authors.urls')),  # <-- Added by your teammate
    
    # API Documentation endpoints (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
