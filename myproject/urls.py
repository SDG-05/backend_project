from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def health_check(request):
    return JsonResponse({"status": "ok", "service": "myproject"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    
    # ==========================================
    # YOUR APPS (categories, expenses, reports)
    # Grouped under: /api/finance/ 
    # (Feel free to change 'finance' to 'my-apps' or 'accounts')
    # ==========================================
    path('api/expense_tracker/', include('categories.urls')),   # -> /api/finance/categories/
    path('api/expense_tracker/', include('expenses.urls')),     # -> /api/finance/expenses/
    path('api/expense_tracker/', include('reports.urls')),      # -> /api/finance/reports/...
    
    # ==========================================
    # TEAMMATE 1 APPS (books, authors, members)
    # Grouped under: /api/teammate1/ 
    # (Change 'teammate1' to their name or 'library')
    # ==========================================
    path('api/library/', include('books.urls')),      
    path('api/library/authors/', include('authors.urls')), 
    path('api/library/members/', include('members.urls')), 
    
    # ==========================================
    # TEAMMATE 2 APPS (urlshortener)
    # Grouped under: /api/teammate2/ 
    # (Change 'teammate2' to their name or 'tools')
    # ==========================================
    path('api/shorturl/', include('urlshortener.urls')), 
    
    # ==========================================
    # API Documentation endpoints (drf-spectacular)
    # ==========================================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]