# quiz/admin.py

from django.contrib import admin
from .models import Subject, Quiz, Question, Answer, TakenQuiz, StudentAnswer

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'classe', 'cours', 'owner', 'status')
    search_fields = ('name', 'subject__name', 'classe__numeroClasse', 'cours__titre', 'owner__username')
    list_filter = ('subject', 'classe', 'cours', 'status')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    search_fields = ('text',)
    list_filter = ('is_correct',)

@admin.register(TakenQuiz)
class TakenQuizAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'percentage', 'date')
    search_fields = ('student__user__username', 'quiz__name')
    list_filter = ('quiz', 'date')

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'answer')
    search_fields = ('student__user__username', 'answer__text')
