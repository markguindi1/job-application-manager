"""email_manager URL Configuration

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
from . import views

app_name = 'email_manager'

urlpatterns = [
    path('', views.EmailAccountsListView.as_view(), name="email_address_list"),
    path('create/', views.EmailAccountCreate.as_view(), name="email_address_create"),
    path('<int:pk>/', views.EmailAccountUpdate.as_view(), name="email_address_update"),
    path('<int:pk>/delete/', views.EmailAccountDelete.as_view(), name="email_address_delete"),
    path('gmail-auth/', views.GmailAuthRedirectView.as_view(), name="gmail_auth"),
    path('oauth2callback/', views.OAuth2CallbackRedirectView.as_view(), name="oauth2callback"),
    path('emails-list/', views.EmailsListView.as_view(), name="email_list"),
    path('email-content/', views.EmailContentView.as_view(), name="email_content"),
]
