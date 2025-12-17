from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    category_number = models.IntegerField()
    
    def __str__(self):
        return self.name
        
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    sub_category_number = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")
    
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100)
    unit_number = models.IntegerField()
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="units")
    
    def __str__(self):
        return self.name
    
class Quiz(models.Model):
    name = models.CharField(max_length=100)
    quiz_number = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="quizzes")
    
    def __str__(self):
        return self.name
    
class Question(models.Model):
    question_number = models.IntegerField(default=0)
    format = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(255)], # Restrict range to 0-255
        default=0
    )
    audio_str = models.CharField(max_length=500, blank=True, null=True, default="")
    instructions = models.TextField(max_length=500000, blank=True,null=True, default="")
    prompt = models.TextField(max_length=5000, blank=True,null=True, default="")
    content = models.TextField(max_length=1000, default="")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    answer_key = models.TextField(max_length=500, default="")
    score = models.IntegerField(default=0, null=True)
    word_scramble_direction = models.CharField(max_length=1, blank=True, null=True, default="")
    timeout = models.IntegerField(default=0, null=True)  # in miliseconds
    button_cloze_options=models.TextField(max_length=200, blank=True, null=True, default="") 
    
    def __str__(self):
        return self.content
    