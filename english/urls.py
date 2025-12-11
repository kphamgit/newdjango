from django.urls import path
from . import views
from django.http import JsonResponse

urlpatterns = [
  
    path("questions/", views.QuestionCreateView.as_view(), name="question-create"),
    path("questions/<int:pk>/", views.QuestionEditView.as_view(), name="question-edit"),
    path("quizzes/", views.QuizCreateView.as_view(), name="quiz-create"),
    path("quizzes/<int:pk>/", views.QuizEditView.as_view(), name="quiz-edit"),
    path("units/", views.UnitCreateView.as_view(), name="unit-create"),
    path("units/<int:pk>/", views.UnitEditView.as_view(), name="unit-edit"),
    path("sub_categories/", views.SubCategoryCreateView.as_view(), name="sub-category-create"),
    path("sub_categories/<int:pk>/", views.SubCategoryEditView.as_view(), name="sub-category-edit"),
    path("categories/", views.CategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/", views.CategoryEditView.as_view(), name="category-edit"),
    
]

