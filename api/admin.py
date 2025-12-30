from django.contrib import admin

# Register your models here.
from .models import Level, Category, Unit, Quiz, Question

admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Quiz)
admin.site.register(Question)

