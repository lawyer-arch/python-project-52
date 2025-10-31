"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from .views import HomePageView, CustomLoginView, CustomLogoutView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", CustomLoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("tasks/", include("tasks.urls")),
    path("labels/", include("labels.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]
