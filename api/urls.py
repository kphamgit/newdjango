from django.urls import path
from . import views
from django.http import JsonResponse

def test_unit_list_view(request, pk):
    return JsonResponse({"message": "Unit List View is working!"})

urlpatterns = [
    #path("categories/", views.CategoryListCreate.as_view(), name="category-list"),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/<int:category_id>/sub_categories", views.SubCategoryListView.as_view(), name="sub-category-list"),
    path("sub_categories/<int:sub_category_id>/units", views.UnitListView.as_view(), name="unit-list"),
    path("units/<int:unit_id>/quizzes", views.QuizListView.as_view(), name="quiz-list"),
    path("quizzes/<int:quiz_id>/questions", views.QuestionListView.as_view(), name="question-list"),
    #path("questions/<int:pk>/", test_unit_list_view , name="question-detail"),
    
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
]

