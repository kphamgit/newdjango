from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer, CategorySerializer, SubCategorySerializer, UnitSerializer, QuizSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, Category, SubCategory, Unit, Quiz, Question


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class CategoryListView(generics.ListAPIView):
    #queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer # needed by the Django REST Framework
    # to determine how to serialize the data returned by the get_queryset method
    
    def get_queryset(self):
        return Category.objects.prefetch_related('subcategories')
    
class UnitListView(generics.ListAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def get_queryset(self):
        sub_category_id = self.kwargs.get('sub_category_id')
        print("UnitListView, sub_category_id:", sub_category_id)
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Unit.objects.filter(sub_category_id=sub_category_id)
        print("UnitListView, Filtered Units no Prefetch:", queryset)
        print("UnitListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def get_queryset(self):
        unit_id = self.kwargs.get('unit_id')
        print("QuizListView, unit_id:", unit_id)
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Quiz.objects.filter(unit_id=unit_id)
        print("QuizListView, Filtered Quizzes no Prefetch:", queryset)
        print("QuizListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        #print("QuestionListView, quiz_id:", quiz_id)
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Question.objects.filter(quiz_id=quiz_id)
        #print("QuestionListView, Filtered Questions no Prefetch:", queryset)
        #print("QuestionListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
            

class SubCategoryListView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        #queryset = Unit.objects.filter(category_id=category_id).prefetch_related('quizzes')
        queryset = SubCategory.objects.filter(category_id=category_id)
        print("Filtered SubCats:", queryset)
        #print("SQL Query:", queryset.query)  # Debugging SQL query
        return queryset