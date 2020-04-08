from django.urls import path

from . import views

urlpatterns = [
    path('request_token/', views.initiate_temporary_credential),
    path('authorize/', views.authorize),
    path('access_token/', views.issue_token),
]
