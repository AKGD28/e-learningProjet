from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe

# Register your models here.
class CustomAdmin(admin.ModelAdmin):
    actions = ('activate','desactivate')
    list_filter = ('status',)
    list_per_page = 10
    date_hierachy = "date_add"

    def activate(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,'la selection a été effectué avec succes')
    activate.short_description = "permet d'activer le champs selectionner"

    def desactivate(self,request,queryset):  
        queryset.update(status=False)
        self.message_user(request,'la selection a été effectué avec succes')
    desactivate.short_description = "permet de desactiver le champs selectionner"


class  MatiereAdmin(CustomAdmin):
    list_display = ('nom','status')
    list_display_links = ['nom',]
    search_fields = ('nom',)
    ordering = ('nom',)
    fieldsets = [
                 ("info matière",{"fields":["nom", "image", "description"]}),
                 ("standard",{"fields":["status"]})
    ]

class NiveauAdmin(CustomAdmin):
    list_display = ('nom','status')
    list_display_links = ['nom',]
    search_fields = ('nom',)
    ordering = ('nom',)
    fieldsets = [
                 ("info niveau",{"fields":["nom"]}),
                 ("standard",{"fields":["status"]})
    ]

class ClasseAdmin(CustomAdmin):
    list_display = ('niveau','numeroClasse','status')
    list_display_links = ['niveau',]
    search_fields = ('niveau',)
    ordering = ('niveau',)
    fieldsets = [
                 ("info classe",{"fields":["niveau","numeroClasse"]}),
                 ("standard",{"fields":["status"]})
    ]

class ChapitreAdmin(CustomAdmin):
    list_display = ('matiere','titre', 'classe', 'video', 'image', 'duree_en_heure', 'date_debut', 'date_fin', 'status')
    list_display_links = ['titre',]
    search_fields = ('titre',)
    ordering = ('titre',)
    fieldsets = [
                 ("info chapitre",{"fields":["matiere", "image", "video", 'duree_en_heure', 'date_debut', 'date_fin', 'classe']}),
                 ("standard",{"fields":["status"]})
    ]

class CoursAdmin(CustomAdmin):
    list_display = ('chapitre','titre','status')
    list_display_links = ['chapitre',]
    search_fields = ('chapitre',)
    ordering = ('chapitre',)
    fieldsets = [
                 ("info cours",{"fields":["chapitre","titre", "image", "video", "pdf"]}),
                 ("standard",{"fields":["status"]})
    ]


def _register(model,admin_class):
    admin.site.register(model,admin_class)


_register(models.Matiere, MatiereAdmin)
_register(models.Niveau, NiveauAdmin)
_register(models.Classe, ClasseAdmin)
_register(models.Chapitre, ChapitreAdmin)
_register(models.Cours, CoursAdmin)



