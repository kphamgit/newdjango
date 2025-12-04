from django.urls import path
from . import views

urlpatterns = [
    #path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    #path("categories/", views.CategoryListDisplay.as_view(), name="category-list"),
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    #path("categories/", views.CategoryListCreate.as_view(), name="category-list"),
    path("units/<int:sub_category_id>/", views.UnitListView.as_view(), name="unit-list"),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
]