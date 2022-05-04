from django.urls import path
from . import views

urlpatterns = [
    # path('notes/<int:pk>', views.GetSpecific.as_view(), name='notes_details'),
    path('notes/', views.Notes.as_view(), name='notes'),
    # path('notedelete/', views.NotesDetails.as_view(), name='notedelete')
]