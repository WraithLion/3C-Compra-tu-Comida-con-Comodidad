"""
URL configuration for sitio_3C project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('',include('app3C.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    # 1. Servir archivos de medios (imágenes subidas) - CORRECTO
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 2. Servir archivos estáticos (CSS/JS) - CORRECTO (Solo esto)
# Elimina la línea de STATIC_ROOT de arriba
if settings.STATICFILES_DIRS:
    # Nota: STATICFILES_DIRS es una lista/tupla, tomamos el primer elemento
    document_root = settings.STATICFILES_DIRS
    urlpatterns += static(settings.STATIC_URL, document_root=document_root)
