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
    
    #create_quiz_attempt
    #path("notes/delete/<int:pk>/", views.NoteDcreate_quiz_attemptelete.as_view(), name="delete-note"),
    #path("quiz_attempts/<int:pk>/create_next_question_attempt/", views.create_question_attempt),  # pk is quiz_attempt_id
    path("quiz_attempts/<int:pk>/", views.create_quiz_attempt),     # pk is quiz_id
    #/api/quiz_attempts/${quiz_attempt_id}/create_next_question_attempt`;
    path("quiz_attempts/<int:pk>/create_next_question_attempt/", views.create_question_attempt),  # pk is quiz_attempt_id
    path("quiz_attempts/<int:pk>/create_next_question_attempt_redo/", views.create_question_attempt_redo),  # pk is quiz_attempt_id
    path("quiz_attempts/<int:pk>/reset/", views.reset_quiz_attempt),  # pk is quiz_attempt_id
    path("quiz_attempts/<int:pk>/continue/", views.continue_quiz_attempt),  # pk is quiz_attempt_id
    path("quiz_attempts/<int:pk>/redo_errorneous_attempts/", views.redo_errorneous_question_attempts),  # pk is quiz_attempt_id
    
    path("question_attempts/<int:pk>/update/", views.update_question_attempt),  # pk is quiz_attempt_id
    path("question_attempts/<int:pk>/update_during_redo/", views.update_question_attempt_redo),  # pk is quiz_attempt_id
] 
    #/api/quiz_attempts/119/redo_errorneous_attempts/ update_during_redo
    #Not Found: /api/question_attempts/298/update_during_redo/