from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name='registration'),

    path('login/', views.LoginView.as_view(), name='login'),
    ]