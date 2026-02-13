"""
URL configuration for garden_timekeeper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import CustomLoginView


urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path('admin/', admin.site.urls),

    path('summernote/', include('django_summernote.urls')),
]

# Allow Django to serve uploaded files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
