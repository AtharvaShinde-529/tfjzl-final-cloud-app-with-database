"""Admin registration for onlinecourse models."""
from django.contrib import admin
from .models import (Course, Lesson, Instructor, Learner,
                     Question, Choice, Submission)

class QuestionInline(admin.StackedInline):
    """Inline editing for questions."""
    model = Question
    extra = 2

class ChoiceInline(admin.StackedInline):
    """Inline editing for choices."""
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """Admin for Question model."""
    inlines = [ChoiceInline]
    list_display = ('content', 'grade', 'course')
    list_filter = ['course']

class LessonInline(admin.StackedInline):
    """Inline editing for lessons."""
    model = Lesson
    extra = 5

class CourseAdmin(admin.ModelAdmin):
    """Admin for Course model."""
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class LessonAdmin(admin.ModelAdmin):
    """Admin for Lesson model."""
    list_display = ['title']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
