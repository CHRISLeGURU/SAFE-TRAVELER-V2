from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.shortcuts import render
from django.templatetags.static import static as static_url
from django.urls import path, include
from safe_traveller.views import SWView

def pwa_manifest(request):
    return JsonResponse({
        "name": "Safe Traveller",
        "short_name": "SafeTraveller",
        "description": "Your intelligent companion for safe and culturally-aware travel",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f172a",
        "theme_color": "#0f172a",
        "orientation": "portrait",
        "scope": "/",
        "icons": [
            {
                "src": static_url("image/icon-192.png"),
                "type": "image/png",
                "sizes": "192x192",
                "purpose": "any maskable"
            },
            {
                "src": static_url("image/icon-512.png"),
                "type": "image/png",
                "sizes": "512x512",
                "purpose": "any maskable"
            }
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('travels/', include('travels.urls')),
    path('map/', include('maps.urls')),
    path('translate/', include('translate.urls')),
    path('manifest.json', pwa_manifest, name='pwa_manifest'),
    path('sw.js', SWView.as_view(), name='service-worker'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
