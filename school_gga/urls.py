"""school_gga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache
#from django.contrib.admin.views.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schoolapp.urls')),
    #path('tinymce/', include('tinymce.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #path('ckeditor/upload/', login_requred(uploader_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

