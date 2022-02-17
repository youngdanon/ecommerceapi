from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from users.api import urls as user_urls
from main.api import urls as shop_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include(user_urls)),
    path('api/v1/product/', include(shop_urls))

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
