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
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from terminology import views
from terminology_service.settings import DEBUG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Сервис терминологии",
      default_version='v1',
      description="База данных справочников, с кодами и значениями",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="terminology@service.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('refbooks/<int:id>/check_element/', views.CheckHandbookElementAPIViev.as_view()),
    path('refbooks/<int:id>/elements/', views.GetHandbookElementAPIViev.as_view()),
    path('refbooks/', views.GetHandbookListAPIView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if DEBUG:
    urlpatterns += [
    # ... the rest of your URLconf goes here ...
    ] + debug_toolbar_urls()

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Администрирование сайта"