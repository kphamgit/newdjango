from django.urls import path
from . import views
from django.http import JsonResponse

urlpatterns = [
    path("levels/", views.level_list, name="level-list"),
    #path("categories/list/", views.category_list, name="category-list"),
    #there is no need SubCategoryListView here as categories/list/ provides categories with subcategories
    path("categories/<int:category_id>/units/", views.UnitListView.as_view(), name="unit-list"),
   
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