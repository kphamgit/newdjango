from rest_framework import serializers
#from .models import Note
from api.models import Unit, Quiz, QuizAttempt

class UnitSerializer(serializers.ModelSerializer):
    #quizzes = QuizSerializer(many=True, read_only=True)
    class Meta:
        model = Unit
        fields = ["id", "sub_category_id", "name", "unit_number"]
        #extra_kwargs = {
        #    "quizzes": {"required": False}  # Make the "questions" field optional
        #}

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "unit_id", "name", "quiz_number"]
        #extra_kwargs = {
        #    "questions": {"required": False}  # Make the "questions" field optional
        #}
        

        
#score | created_at | updated_at | questions_exhausted | quiz_id | user_id | completion_status | errorneous_questions 