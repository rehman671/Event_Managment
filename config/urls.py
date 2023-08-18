from django.contrib import admin
from django.urls import include, path

# API URLS
urlpatterns = [path("admin/", admin.site.urls), path("api/", include("user.urls"))]
