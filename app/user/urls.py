"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user' #app name

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'), #connecting to views.py in user
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]