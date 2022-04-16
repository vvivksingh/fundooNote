from django.urls import path
from . import views

urlpatterns = [
    path('notes', views.Notes.as_view(), name='notes')
]