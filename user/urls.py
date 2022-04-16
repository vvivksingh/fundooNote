from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name='registration'),
<<<<<<< HEAD
=======
    path('login/', views.LoginView.as_view(), name='login'),
>>>>>>> userLogin
    ]