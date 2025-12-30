from rest_framework import serializers
#from .models import Note
from api.models import Unit, Quiz, SubCategory, Category, Level

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "unit_id", "name", "quiz_number"]
        #extra_kwargs = {
        #    "questions": {"required": False}  # Make the "questions" field optional
        #}

class UnitSerializer(serializers.ModelSerializer):
    #quizzes = QuizSerializer(many=True, read_only=True)
    class Meta:
        model = Unit
        fields = ["id", "category_id", "name", "unit_number"]
        #extra_kwargs = {
        #    "units": {"required": False}  # Make the "questions" field optional
        #}

"""
class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    print("Inside ENGLISH CategorySerializer")
    class Meta:
        model = Category
        fields = ["id", "name", "category_number", "sub_categories"]

    def __init__(self, *args, **kwargs):
        # Dynamically exclude sub_categories if specified in the context
        exclude_sub_categories = kwargs.pop('context', {}).get('exclude_sub_categories', False)
        super().__init__(*args, **kwargs)
        if exclude_sub_categories:
            self.fields.pop('sub_categories', None)  # Remove the sub_categories field
"""
class CategorySerializer(serializers.ModelSerializer):
    #sub_categories = SubCategorySerializer(many=True, read_only=True)
    #print("Inside ENGLISH ... CategorySerializer")
    class Meta:
        model = Category
        fields = ["id", "level_id", "name", "category_number"]
        
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "name", "level_number"]
