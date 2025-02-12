from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tg_bot.views import me_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('app.internal.urls')),
    path("me/", me_view, name="me"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
