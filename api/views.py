from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer, CategorySerializer, UnitSerializer
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

    def get_queryset(self):
        sub_category_id = self.kwargs.get('sub_category_id')
        queryset = Unit.objects.filter(sub_category_id=sub_category_id).prefetch_related('quizzes')
        print("Filtered Units with Prefetch:", queryset)
        print("SQL Query:", queryset.query)  # Debugging SQL query
        return queryset