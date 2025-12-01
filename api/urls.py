from django.urls import path
from . import views

urlpatterns = [
    #path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    #path("categories/", views.CategoryListDisplay.as_view(), name="category-list"),
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("categories/", views.CategoryListCreate.as_view(), name="category-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
]