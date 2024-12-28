# student/admin.py

from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classe', 'score', 'status')
    search_fields = ('user__username', 'bio', 'ville')
    list_filter = ('classe', 'status')

