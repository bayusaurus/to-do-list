from django.urls import path, include
from django.conf import settings
from notes.views import *

urlpatterns = [
    # path('login/', Login.as_view(), name='Login'),
    path('', Dashboard.as_view(), name='dashboard'),
    path('register/', Register.as_view(), name='register'),
    path('notes/create/', NotesCreate.as_view(), name='notes_create'),
    path('notes/edit/<str:id>', NotesEdit.as_view(), name='notes_edit'),
    path('notes/flag_delete/', NotesFlagDelete.as_view(), name='notes_flag_delete'),
    path('notes/reorder/', NotesReorder.as_view(), name='notes_reorder'),
]
