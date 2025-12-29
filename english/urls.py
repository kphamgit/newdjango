from django.urls import path
from . import views
from django.http import JsonResponse

urlpatterns = [

    # LIST views
    
    path("categories/list/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/sub_categories/", views.SubCategoryListView.as_view(), name="sub-category-list"),
    path("sub_categories/<int:pk>/units/", views.UnitListView.as_view(), name="unit-list"),
    path("units/<int:pk>/quizzes", views.QuizListView.as_view(), name="quiz-list"),
    path("quizzes/<int:pk>/questions", views.QuestionListView.as_view(), name="question-list"),
    # end LIST views
    path("questions/", views.QuestionCreateView.as_view(), name="question-create"),
    path("questions/<int:pk>/", views.QuestionEditView.as_view(), name="question-edit"),
    path("quizzes/", views.QuizCreateView.as_view(), name="quiz-create"),
    path("quizzes/<int:pk>/", views.QuizEditView.as_view(), name="quiz-edit"),
    path("units/", views.UnitCreateView.as_view(), name="unit-create"),
    path("units/<int:pk>/", views.UnitEditView.as_view(), name="unit-edit"),
  
    path("quiz_attempts/", views.quiz_attempt_list),
    #path("quiz_attempts/<int:pk>/delete", views.quiz_attempt_delete),
    path("quiz_attempts/bulk_delete/", views.quiz_attempt_bulk_delete),
    path("quiz_attempts/<int:pk>/question_attempts/", views.quiz_attempt_get_question_attempts),

    # CREATE
    path("categories/", views.CategoryCreateView.as_view(), name="category-create"),
    path("sub_categories/", views.SubCategoryCreateView.as_view(), name="sub-category-create"),
    path("sub_categories/<int:pk>/", views.SubCategoryEditView.as_view(), name="sub-category-edit"),
    path("categories/<int:pk>/", views.CategoryEditView.as_view(), name="category-edit"),

    path("items/delete/<int:pk>/", views.ItemDeleteView.as_view(), name="item-delete"),
    # item can be : category, sub_category, unit, quiz, question
    # utilities
    path("category/renumber", views.CategoryRenumberView.as_view(), name="categories-renumber"),
    path("sub_category/renumber", views.SubCategoryRenumberView.as_view(), name="sub-categories-renumber"),
    path("unit/renumber", views.UnitRenumberView.as_view(), name="units-renumber"),
    path("quiz/renumber", views.QuizRenumberView.as_view(), name="quizzes-renumber"),
    path("question/renumber", views.QuestionRenumberView.as_view(), name="question-renumber"),


]

