from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Salon)
class SalonAdmin(admin.ModelAdmin):

    list_display = ('nom', 'classe', 'date_add','status',)
    list_filter = ('status',)
    list_filter = ('status',)

    #  CHAMPS DE RECHERCHE DU MODEL DANS L'ADMIN #
    
    search_field = ('projet', 'nom')
#     fieldsets = [
#         ('les clés etrangeres', {'fields': ['projets', 'developpeurs', 'taches','user',]}),
#         ('les champs specifiques', {'fields': ['is_view', 'message',]}),
#         ('les champs standards', {'fields': ['date_add', 'status',]}),
#     ]

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ('auteur', 'message', 'salon','status',)
    list_filter = ('status',)
    list_filter = ('status',)

    #  CHAMPS DE RECHERCHE DU MODEL DANS L'ADMIN #
    
    search_field = ('salon', 'nom')
#     fieldsets = [
#         ('les clés etrangeres', {'fields': ['projets', 'developpeurs', 'taches','user',]}),
#         ('les champs specifiques', {'fields': ['is_view', 'message',]}),
#         ('les champs standards', {'fields': ['date_add', 'status',]}),
#     ]