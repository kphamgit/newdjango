from django.shortcuts import render
from api.models import Note, Question, Quiz, Unit, SubCategory, Category
#from .serializers import NoteSerializer, QuestionSerializer
from api.serializers import NoteSerializer, QuestionSerializer, QuizSerializer, UnitSerializer, SubCategorySerializer, CategorySerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

# Create your views here.
   
# LIST/CREATE VIEWS
 
class QuestionCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(question_number=self.request.data.get('question_number'),
                            format=self.request.data.get('format'),
                            audio_str=self.request.data.get('audio_str'),
                            instructions=self.request.data.get('instructions'),
                            prompt=self.request.data.get('prompt'),
                            content=self.request.data.get('content'),
                            quiz_id=self.request.data.get('quiz_id'),
                            answer_key=self.request.data.get('answer_key')
            )
        else:
            print(serializer.errors)

    
class QuizCreateView(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(quiz_number=self.request.data.get('quiz_number'),
                            name=self.request.data.get('name')
            )
        else:
            print(serializer.errors)
            
class UnitCreateView(generics.ListCreateAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(unit_number=self.request.data.get('unit_number'),
                            name=self.request.data.get('name')
            )
        else:
            print(serializer.errors)
            
class SubCategoryCreateView(generics.ListCreateAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(sub_category_number=self.request.data.get('sub_category_number'),
                            name=self.request.data.get('name')
            )
        else:
            print(serializer.errors)
            
class CategoryCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(category_number=self.request.data.get('category_number'),
                            name=self.request.data.get('name')
            )
        else:
            print(serializer.errors)

# EDIT/UPDATE VIEWS

class QuestionEditView(generics.RetrieveUpdateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    #queryset = Question.objects.filter(question_id=question_id)  # Add this line
    #print("QuestionEditView HERE")
    def perform_update(self, serializer):
        #print("request data:", self.request.data)
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save(
                            audio_str=self.request.data.get('audio_str'),
                            prompt=self.request.data.get('prompt'),
                            content=self.request.data.get('content'),
                            answer_key=self.request.data.get('answer_key')
            )
        else:
            print(serializer.errors)
            
    def get_queryset(self):
        question_id = self.kwargs.get('pk')
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Question.objects.filter(id=question_id)
        #print("QuestionListView, Filtered Questions no Prefetch:", queryset)
        #print("QuestionListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
class QuizEditView(generics.RetrieveUpdateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    #queryset = Question.objects.filter(question_id=question_id)  # Add this line
    def perform_update(self, serializer):
        #print("request data:", self.request.data)
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save(
                name=self.request.data.get('name'),
            )
        else:
            print(serializer.errors)
            
    def get_queryset(self):
        quiz_id = self.kwargs.get('pk')
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Quiz.objects.filter(id=quiz_id)
        #print("QuestionListView, Filtered Questions no Prefetch:", queryset)
        #print("QuestionListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
class UnitEditView(generics.RetrieveUpdateAPIView):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    #queryset = Question.objects.filter(question_id=question_id)  # Add this line
    def perform_update(self, serializer):
        #print("request data:", self.request.data)
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save(
                name=self.request.data.get('name'),
            )
        else:
            print(serializer.errors)
            
    def get_queryset(self):
        unit_id = self.kwargs.get('pk')
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Unit.objects.filter(id=unit_id)
        #print("QuestionListView, Filtered Questions no Prefetch:", queryset)
        #print("QuestionListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
class SubCategoryEditView(generics.RetrieveUpdateAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]
    #queryset = Question.objects.filter(question_id=question_id)  # Add this line
    def perform_update(self, serializer):
        #print("request data:", self.request.data)
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save(
                name=self.request.data.get('name'),
            )
        else:
            print(serializer.errors)
            
    def get_queryset(self):
        sub_category_id = self.kwargs.get('pk')
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = SubCategory.objects.filter(id=sub_category_id)
        #print("QuestionListView, Filtered Questions no Prefetch:", queryset)
        #print("QuestionListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    
class CategoryEditView(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    #queryset = Question.objects.filter(question_id=question_id)  # Add this line
    def perform_update(self, serializer):
        print("request data:", self.request.data)
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save(
                name=self.request.data.get('name'),
            )
        else:
            print(serializer.errors)
            
    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        print("XXXXXX category_id:", category_id)
        #queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        queryset = Category.objects.filter(id=category_id)
        #print("QuestionListView, Filtered Questions no Prefetch:", queryset)
        #print("QuestionListView, SQL Query:", queryset.query)  # Debugging SQL query
        return queryset
    