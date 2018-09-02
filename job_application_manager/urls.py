"""job_application_manager URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from email_manager.gmail_api_auth_files.authentication_views import oauth2callback

urlpatterns = [
    path('', include('application_manager.homepage_urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user_accounts.urls')),
    path('application/', include('application_manager.urls')),
    path('email/', include('email_manager.urls')),
    path('oauth2callback/', oauth2callback, name="oauth2callback"),
]
