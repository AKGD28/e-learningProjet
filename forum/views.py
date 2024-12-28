# views.py (exemple)
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Sujet  # ou le modèle correspondant

def forum(request):
    # 1) Récupérez vos QuerySets
    # Exemple : sujets “généraux”
    forum_general_qs = Sujet.objects.filter(cours__isnull=True).order_by('-date_add')
    # Exemple : sujets “Lessons”
    forum_lessons_qs = Sujet.objects.filter(cours__isnull=False).order_by('-date_add')

    # 2) Définir la pagination pour forum_general
    page_number_general = request.GET.get('page_g')  # clé GET distincte, ex: ?page_g=2
    paginator_general = Paginator(forum_general_qs, 5)  # 5 éléments par page
    forum_general_page = paginator_general.get_page(page_number_general)

    # 3) Définir la pagination pour forum_lessons
    page_number_lessons = request.GET.get('page_l')  # ex: ?page_l=3
    paginator_lessons = Paginator(forum_lessons_qs, 5)
    forum_lessons_page = paginator_lessons.get_page(page_number_lessons)

    context = {
        'forum_general': forum_general_page,  # <= On passe l'OBJET de type Page
        'forum': forum_lessons_page,
    }
    return render(request, 'fixed-student-forum.html', context)