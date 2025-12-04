from django.contrib import admin

# Register your models here.
from .models import Note, Category, SubCategory, Unit, Quiz, Question

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Unit)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Note)
