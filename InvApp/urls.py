from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventory.views import index

urlpatterns = [
    path('', include('accounts.urls')),
    path('dashboard', index, name='index'),
    path('inventory/', include('inventory.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
