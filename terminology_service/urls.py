"""
URL configuration for terminology_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from terminology import views
from terminology_service.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
#    re_path(r'^refbooks/(?P<year>[0-9]{4})-(?P<month>[0-1][0-9])-(?P<day>[0-3][0-9])', views.HandbookListAPIView.as_view())
    path('refbooks/<int:id>/elements/', views.HandbookElementAPIViev.as_view()),
    path('refbooks/', views.HandbookListAPIView.as_view())
]

if DEBUG:
    urlpatterns += [
    # ... the rest of your URLconf goes here ...
    ] + debug_toolbar_urls()

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Администрирование сайта"