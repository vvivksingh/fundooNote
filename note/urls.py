from django.urls import path
from . import views

urlpatterns = [
    path('notes/<int:pk>', views.GetSpecific.as_view(), name='notes_details'),
    path('notes/', views.Notes.as_view(), name='notes'),
    # path('notes/updatecolor/<int:pk>',views.ColorUpdate.as_view(), name='notes_color'),
    # path('notes/updatearchieve/<int:pk>',views.ArchieveUpdate.as_view(), name='notes_color'),


    # path('notedelete/', views.NotesDetails.as_view(), name='notedelete')
]