from django.contrib import admin
from django.urls import path, include

import authentication.urls
import core.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth', include(authentication.urls, namespace='auth')),
    path('api/', include(core.urls, namespace='core')),
]
