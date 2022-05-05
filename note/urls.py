from django.urls import path
from . import views

urlpatterns = [
    path('delnotes/', views.DeleteSpecific.as_view(), name='delnotes'),
    path('notes/', views.Notes.as_view(), name='notes')
]