# instructor/admin.py

from django.contrib import admin
from .models import Instructor

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'adresse', 'classe', 'status', 'date_add')
    search_fields = ('user__username', 'contact', 'adresse', 'bio', 'ville')
    list_filter = ('classe', 'status', 'date_add', 'date_update')
    readonly_fields = ('date_add', 'date_update', 'slug')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "Les instructeurs sélectionnés sont maintenant actifs.")

    make_active.short_description = "Marquer les instructeurs sélectionnés comme actifs"

    def make_inactive(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "Les instructeurs sélectionnés sont maintenant inactifs.")

    make_inactive.short_description = "Marquer les instructeurs sélectionnés comme inactifs"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('slug',)
        return self.readonly_fields
