from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Category, SubCategory, Unit, Quiz, Question


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

        
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_number", "content"]
        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "name", "quiz_number"]
        

class UnitSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)
    class Meta:
        model = Unit
        fields = ["id", "name", "unit_number", "sub_category", "quizzes"]
        
        
class SubCategorySerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ["id", "name", "sub_category_number", "units"]
        
class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["id", "name", "category_number", "subcategories"]
        #extra_kwargs = {"author": {"read_only": True}}