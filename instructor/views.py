from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.db.models import Q
from django.utils.safestring import mark_safe
import json
from django.db.models import Avg, Count

# Imports
from django.contrib.auth.models import User
from school import models as school_models
from quiz import models as quiz_models
from forum import models as forum_models
from chat import models as chat_models
from . import models  # instructor.models (Instructor)
from student.models import Student

########################################
#   PROFIL & DASHBOARD
########################################

@login_required(login_url='login')
def profile(request):
    """
    Vue pour afficher le profil de l'instructeur.
    Redirige un étudiant ou un admin si nécessaire.
    """
    # Si l'utilisateur est un étudiant
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')

    # Si c'est un instructeur
    elif hasattr(request.user, 'instructor'):
        datas = {
            'instructor': request.user.instructor,
        }
        return render(request, 'pages/instructor-profile.html', datas)
    else:
        # Admin/staff ou autre
        return redirect('/admin/')

@login_required(login_url='login')
def dashboard(request):
    """
    Dashboard de l'instructeur.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        matiere = school_models.Matiere.objects.filter(status=True)
        datas = {
            'matiere': matiere
        }
        return render(request, 'pages/instructor-dashboard.html', datas)
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def account_edit(request):
    """
    Édition du compte instructeur.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        datas = {
            'instructor': request.user.instructor
        }
        return render(request, 'pages/instructor-account-edit.html', datas)
    else:
        return redirect('/admin/')


########################################
#   GESTION DES CHAPITRES / COURS
########################################

@login_required(login_url='login')
def course_add(request):
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        # Exemple : on affiche la liste des matières
        matiere = school_models.Matiere.objects.filter(status=True)
        datas = {
            'matiere': matiere,
        }
        return render(request, 'pages/instructor-course-add.html', datas)
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def course_edit(request, slug):
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        matiere = school_models.Matiere.objects.filter(status=True)
        chapitre = get_object_or_404(school_models.Chapitre, slug=slug)
        datas = {
            'matiere': matiere,
            'chapitre': chapitre,
        }
        return render(request, 'pages/instructor-course-edit.html', datas)
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def courses(request):
    """
    Liste des chapitres pour la classe de l'instructeur.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        chapitres = school_models.Chapitre.objects.filter(
            Q(status=True) & Q(classe=request.user.instructor.classe)
        )
        datas = {
            'Chapitre': chapitres
        }
        return render(request, 'pages/instructor-courses.html', datas)
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def matiere(request, slug):
    """
    Liste des chapitres d'une matière donnée.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        chapitres = school_models.Chapitre.objects.filter(
            Q(status=True) &
            Q(classe=request.user.instructor.classe) &
            Q(matiere__slug=slug)
        )
        datas = {
            'Chapitre': chapitres
        }
        return render(request, 'pages/instructor-cours-chap.html', datas)
    else:
        return redirect('/admin/')


########################################
#   GESTION DES LEÇONS
########################################

@login_required(login_url='login')
def lesson_add(request, slug):
    """
    Form pour ajouter un Cours (lesson) à un Chapitre identifié par son slug.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        chapitre = get_object_or_404(school_models.Chapitre, slug=slug)
        datas = {
            'chapitre': chapitre
        }
        return render(request, 'pages/instructor-lesson-add.html', datas)
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def lesson_edit(request, id, slug):
    """
    Éditer une leçon (Cours):
    - 'id' est l'ID du chapitre
    - 'slug' est le slug du cours
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        chapitre = get_object_or_404(school_models.Chapitre, id=id)
        cours = get_object_or_404(school_models.Cours, slug=slug)
        datas = {
            'chapitre': chapitre,
            'cours': cours
        }
        return render(request, 'pages/instructor-lesson-edit.html', datas)
    else:
        return redirect('/admin/')


########################################
#   GESTION DES QUIZ
########################################

@login_required(login_url='login')
def quizzes(request):
    """
    Liste de tous les quiz créés par l'instructeur.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        quizzes = quiz_models.Quiz.objects.filter(owner=request.user)
        datas = {
            'quizzes': quizzes
        }
        return render(request, 'pages/instructor-quizzes.html', datas)
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def quiz_add(request):
    """
    Ajout d'un nouveau quiz.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        if request.method == 'POST':
            # Récupérer les données du formulaire
            name = request.POST.get('name')
            subject_id = request.POST.get('subject_id')
            cours_id = request.POST.get('cours_id')

            # Vérifier que les données sont valides
            try:
                subject = quiz_models.Subject.objects.get(id=subject_id)
                cours = school_models.Cours.objects.get(id=cours_id)
            except Exception as e:
                print(e)
                return redirect('instructor-quiz-add')

            # Créer le quiz
            quiz = quiz_models.Quiz.objects.create(
                owner=request.user,
                name=name,
                subject=subject,
                classe=request.user.instructor.classe,
                cours=cours
            )

            # Rediriger vers la gestion des questions
            return redirect('quiz_edit_questions', quiz_id=quiz.id)
        else:
            # Préparer les données pour le formulaire
            subjects = quiz_models.Subject.objects.all()
            cours_list = school_models.Cours.objects.filter(
                chapitre__classe=request.user.instructor.classe
            )
            datas = {
                'subjects': subjects,
                'cours_list': cours_list
            }
            return render(request, 'pages/instructor-quiz-add.html', datas)
    else:
        return redirect('/admin/')    


    
def quiz_edit(request, quiz_id):
    quiz = get_object_or_404(quiz_models.Quiz, id=quiz_id, owner=request.user)

    if request.method == 'POST':
        quiz.name = request.POST.get('name', quiz.name)
        subject_id = request.POST.get('subject_id')
        cours_id = request.POST.get('cours_id')
        if subject_id:
            try:
                subject = quiz_models.Subject.objects.get(id=subject_id)
                quiz.subject = subject
            except:
                pass
        if cours_id:
            try:
                cours = school_models.Cours.objects.get(id=cours_id)
                quiz.cours = cours
            except:
                pass
        quiz.save()
        return redirect('instructor-quizzes')
    else:
        subjects = quiz_models.Subject.objects.all()
        cours_list = school_models.Cours.objects.filter(
            chapitre__classe=request.user.instructor.classe
        )
        datas = {
            'quiz': quiz,
            'subjects': subjects,
            'cours_list': cours_list
        }
        return render(request, 'pages/instructor-quiz-edit.html', datas)

@login_required(login_url='login')
def review_quiz(request):
    """
    Page pour voir les résultats des quiz (TakenQuiz) pour l'instructeur.
    """
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        quizzes = quiz_models.Quiz.objects.filter(owner=request.user)
        taken_quizzes = quiz_models.TakenQuiz.objects.filter(quiz__in=quizzes).select_related('student', 'quiz')
        datas = {
            'taken_quizzes': taken_quizzes,
        }
        return render(request, 'pages/instructor-review-quiz.html', datas)
    else:
        return redirect('/admin/')


########################################
#   GESTION DES QUESTIONS (NOUVEAU)
########################################

@login_required(login_url='login')
def quiz_edit_questions(request, quiz_id):
    """
    Liste et gestion des questions pour un quiz donné.
    """
    if not hasattr(request.user, 'instructor'):
        return redirect('index_student')

    quiz = get_object_or_404(quiz_models.Quiz, id=quiz_id, owner=request.user)
    questions = quiz.questions.all().order_by('id')
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'pages/instructor-quiz-edit-questions.html', context)

# instructor/views.py

@login_required(login_url='login')
def question_add(request, quiz_id):
    """
    Ajout d'une question à un quiz donné.
    """
    if not hasattr(request.user, 'instructor'):
        return redirect('index_student')

    quiz = get_object_or_404(quiz_models.Quiz, id=quiz_id, owner=request.user)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            quiz_models.Question.objects.create(
                quiz=quiz,
                text=text
            )
        return redirect('quiz_edit_questions', quiz_id=quiz.id)
    else:
        return render(request, 'pages/instructor-question-add.html', {'quiz': quiz})



@login_required(login_url='login')
def question_edit(request, quiz_id, question_id):
    """
    Modification d'une question et gestion de ses réponses.
    """
    if not hasattr(request.user, 'instructor'):
        return redirect('index_student')

    quiz = get_object_or_404(quiz_models.Quiz, id=quiz_id, owner=request.user)
    question = get_object_or_404(quiz_models.Question, id=question_id, quiz=quiz)
    answers = question.answers.all().order_by('id')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            question.text = text
            question.save()
        return redirect('question_edit', quiz_id=quiz.id, question_id=question.id)
    else:
        context = {
            'quiz': quiz,
            'question': question,
            'answers': answers
        }
        return render(request, 'pages/question-edit-with-answers.html', context)



@login_required(login_url='login')
def question_delete(request):
    """
    Suppression d'une question via POST ou AJAX.
    """
    if not hasattr(request.user, 'instructor'):
        return JsonResponse({'success': False, 'message': 'Non autorisé.'})

    question_id = request.POST.get('question_id')
    try:
        question = quiz_models.Question.objects.get(
            id=question_id,
            quiz__owner=request.user
        )
        question.delete()
        return JsonResponse({'success': True, 'message': 'Question supprimée avec succès.'})
    except quiz_models.Question.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cette question n’existe pas.'})

    

def quiz_results(request, quiz_id):
    # Vérification que l'utilisateur est un instructeur
    if not hasattr(request.user, 'instructor'):
        return redirect('index_student')

    # Récupérer le quiz par son ID
    quiz = get_object_or_404(
        quiz_models.Quiz,
        id=quiz_id,
        owner=request.user  # Vérification de la propriété
    )

    # Récupération des résultats associés (TakenQuiz)
    taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
    total_taken_quizzes = taken_quizzes.count()

    # Calcul du score moyen
    quiz_score = taken_quizzes.aggregate(average_score=Avg('score'))['average_score']

    # Passer les données au template
    context = {
        'quiz': quiz,
        'taken_quizzes': taken_quizzes,
        'total_taken_quizzes': total_taken_quizzes,
        'quiz_score': quiz_score,
    }
    return render(request, 'pages/instructor-quiz-results.html', context)

########################################
#   GESTION DU FORUM
########################################

@login_required(login_url='login')
def forum(request):
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        forum_general = forum_models.Sujet.objects.filter(cours=None)
        forum_classe = forum_models.Sujet.objects.filter(
            cours__chapitre__classe=request.user.instructor.classe
        )
        datas = {
            'forum_general': forum_general,
            'forum': forum_classe,
        }
        return render(request, 'pages/instructor-forum.html', datas)
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def forum_ask(request):
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        return render(request, 'pages/instructor-forum-ask.html', {})
    else:
        return redirect('/admin/')

@login_required(login_url='login')
def forum_thread(request, slug):
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        forum = get_object_or_404(forum_models.Sujet, slug=slug)
        datas = {
            'forum': forum
        }
        return render(request, 'pages/instructor-forum-thread.html', datas)
    else:
        return redirect('/admin/')


########################################
#   GESTION DES MESSAGES (CHAT)
########################################

@login_required(login_url='login')
def messages(request, classe):
    if hasattr(request.user, 'student_user'):
        return redirect('index_student')
    elif hasattr(request.user, 'instructor'):
        try:
            exist_classe = chat_models.Salon.objects.get(classe=request.user.instructor.classe)
            info = school_models.Classe.objects.get(id=request.user.instructor.classe.id)
            datas = {
                'info_classe': info,
                'classe': exist_classe,
                'classe_json': mark_safe(json.dumps(exist_classe.id)),
                'username': mark_safe(json.dumps(request.user.username))
            }
            return render(request, 'pages/instructor-messages.html', datas)
        except Exception as e:
            print(e)
            return redirect('/admin/')
    else:
        return redirect('/admin/')


########################################
#   POST / AJAX (Chapitre, Lesson, Profil, etc.)
########################################

def post_cours(request):
    """
    Création ou mise à jour d'un chapitre (Chapitre).
    """
    title = request.POST.get("title") 
    matiere = request.POST.get("matiere")
    date_fin = request.POST.get("date_fin")
    description = request.POST.get("description")
    date_debut = request.POST.get("date_debut")
    duration = request.POST.get("duration")
    chapitre_id = request.POST.get("id")  # id du chapitre s'il existe déjà

    success = False
    message = ""
    chapitre = None

    # Mise à jour d'un chapitre existant ?
    if chapitre_id:
        try:
            chapitre = school_models.Chapitre.objects.get(id=chapitre_id)
            chapitre.titre = title
            chapitre.duree_en_heure = duration
            chapitre.description = description
            mat = school_models.Matiere.objects.get(id=int(matiere))
            chapitre.matiere = mat
            chapitre.classe = request.user.instructor.classe
            # Fichiers
            try:
                chapitre.video = request.FILES["file"]
            except:
                pass
            try:
                chapitre.image = request.FILES["image"]
            except:
                pass
            if date_debut:
                chapitre.date_debut = date_debut
            if date_fin:
                chapitre.date_fin = date_fin
            chapitre.save()
            success = True
            message = 'Mise à jour effectuée avec succès'
        except Exception as e:
            print(e)
            success = False
            message = "Erreur lors de la mise à jour du chapitre"
    else:
        # Création d'un nouveau chapitre
        try:
            chapitre = school_models.Chapitre()
            chapitre.titre = title
            chapitre.duree_en_heure = duration
            chapitre.description = description
            chapitre.classe = request.user.instructor.classe
            mat = school_models.Matiere.objects.get(id=int(matiere))
            chapitre.matiere = mat
            if date_debut:
                chapitre.date_debut = date_debut
            if date_fin:
                chapitre.date_fin = date_fin
            # Fichiers
            try:
                chapitre.video = request.FILES["file"]
            except:
                pass
            try:
                chapitre.image = request.FILES["image"]
            except:
                pass
            chapitre.save()
            success = True
            message = 'Chapitre ajouté avec succès'
        except Exception as e:
            print(e)
            success = False
            message = "Erreur lors de l'ajout du chapitre"

    data = {
        'success': success,
        'message': message,
        'slug': chapitre.slug if chapitre else ""
    }
    return JsonResponse(data, safe=False)


def delete_chapitre(request):
    chapitre_id = request.POST.get("id")
    success = False
    message = ""
    try:
        chapitre = school_models.Chapitre.objects.get(id=int(chapitre_id))
        chapitre.delete()
        success = True
        message = "Le chapitre a bien été supprimé"
    except Exception as e:
        print(e)
        success = False
        message = "Une erreur s'est produite lors de la suppression"
    data = {
        'success': success,
        'message': message
    }
    return JsonResponse(data, safe=False)


def post_lesson(request):
    title = request.POST.get("title")
    chapitre_id = request.POST.get("chapitre")
    description = request.POST.get("description")
    cours_id = request.POST.get("id")

    success = False
    message = ""

    # Mise à jour ?
    if cours_id:
        try:
            cours = school_models.Cours.objects.get(
                Q(id=int(cours_id)) & Q(chapitre__id=int(chapitre_id))
            )
            try:
                cours.video = request.FILES["file"]
            except:
                pass
            try:
                cours.image = request.FILES["image"]
            except:
                pass
            try:
                cours.pdf = request.FILES["pdf"]
            except:
                pass
            cours.titre = title
            cours.description = description
            cours.save()
            success = True
            message = 'Mise à jour effectuée avec succès'
        except Exception as e:
            print(e)
            success = False
            message = "Erreur lors de la mise à jour du cours"
    else:
        # Ajout
        try:
            cours = school_models.Cours()
            chapitre = school_models.Chapitre.objects.get(id=int(chapitre_id))
            cours.chapitre = chapitre
            cours.titre = title
            cours.description = description
            try:
                cours.video = request.FILES["file"]
            except:
                pass
            try:
                cours.image = request.FILES["image"]
            except:
                pass
            try:
                cours.pdf = request.FILES["pdf"]
            except:
                pass
            cours.save()
            success = True
            message = 'Cours ajouté avec succès'
        except Exception as e:
            print(e)
            success = False
            message = "Une erreur s'est produite lors de l'ajout du cours"

    data = {
        'success': success,
        'message': message
    }
    return JsonResponse(data, safe=False)


def delete_lesson(request):
    lesson_id = request.POST.get("id")
    success = False
    message = ""
    try:
        lesson = school_models.Cours.objects.get(id=int(lesson_id))
        lesson.delete()
        success = True
        message = "La leçon a bien été supprimée"
    except Exception as e:
        print(e)
        success = False
        message = "Une erreur s'est produite"
    data = {
        'success': success,
        'message': message
    }
    return JsonResponse(data, safe=False)


########################################
#   UPDATE PROFIL & PASSWORD
########################################

def update_profil(request):
    nom = request.POST.get("nom")
    prenom = request.POST.get("prenom")
    email = request.POST.get("email")
    bio = request.POST.get("bio")

    try:
        user = User.objects.get(username=request.user.username)
        user.last_name = nom
        user.first_name = prenom
        user.email = email
        user.save()

        instructor = models.Instructor.objects.get(user__id=request.user.id)
        instructor.bio = bio
        try:
            image = request.FILES["file"]
            instructor.photo = image
        except:
            pass
        instructor.save()

        success = True
        message = "Vos informations ont été modifiées avec succès"
    except Exception as e:
        print(e)
        success = False
        message = "Une erreur est survenue lors de la mise à jour"

    data = {
        "success": success,
        "message": message
    }
    return JsonResponse(data, safe=False)


def update_password(request):
    last_password = request.POST.get("last_password")
    new_password = request.POST.get("new_password")
    confirm_password = request.POST.get("confirm_password")

    try:
        if not request.user.check_password(last_password):
            success = False
            message = "Ancien mot de passe incorrect"
        elif new_password != confirm_password:
            success = False
            message = "Les mots de passe ne correspondent pas"
        else:
            user = User.objects.get(username=request.user.username)
            user.set_password(new_password)
            user.save()
            user = authenticate(username=user.username, password=new_password)
            if user:
                login(request, user)
            success = True
            message = "Mot de passe modifié avec succès"
    except Exception as e:
        print(e)
        success = False
        message = "Une erreur est survenue lors de la mise à jour"

    data = {
        "success": success,
        "message": message
    }
    return JsonResponse(data, safe=False)


########################################
#   AJOUT D’UN SUJET DE FORUM
########################################

def post_forum(request):
    titre = request.POST.get("titre")
    question = request.POST.get("question")

    success = False
    message = ""
    val = ""

    try:
        forum = forum_models.Sujet.objects.create(
            titre=titre,
            question=question,
            user=request.user
        )
        val = forum.slug
        success = True
        message = "Votre sujet a bien été ajouté!"
    except Exception as e:
        print(e)
        success = False
        message = "Une erreur est survenue lors de la soumission"

    data = {
        "success": success,
        "message": message,
        "forum": val
    }
    return JsonResponse(data, safe=False)


########################################
#   AJOUT De Reponse
########################################


@login_required(login_url='login')
def answer_delete(request):
    """
    Suppression d'une réponse via POST ou AJAX.
    """
    if not hasattr(request.user, 'instructor'):
        return JsonResponse({'success': False, 'message': 'Non autorisé.'})

    answer_id = request.POST.get('answer_id')
    try:
        answer = quiz_models.Answer.objects.get(
            id=answer_id,
            question__quiz__owner=request.user
        )
        answer.delete()
        return JsonResponse({'success': True, 'message': 'Réponse supprimée avec succès.'})
    except quiz_models.Answer.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cette réponse n’existe pas.'})

@login_required(login_url='login')
def answer_edit(request, quiz_id, question_id, answer_id):
    """
    Modification d'une réponse existante.
    """
    if not hasattr(request.user, 'instructor'):
        return redirect('index_student')

    quiz = get_object_or_404(quiz_models.Quiz, id=quiz_id, owner=request.user)
    question = get_object_or_404(quiz_models.Question, id=question_id, quiz=quiz)
    answer = get_object_or_404(quiz_models.Answer, id=answer_id, question=question)

    if request.method == 'POST':
        text = request.POST.get('text')
        is_correct = request.POST.get('is_correct', 'false').lower() in ['true', 'on', '1']

        if text:
            answer.text = text
            answer.is_correct = is_correct
            answer.save()
        return redirect('answer_list', quiz_id=quiz.id, question_id=question.id)
    else:
        context = {
            'quiz': quiz,
            'question': question,
            'answer': answer
        }
        return render(request, 'pages/answer-edit.html', context)



@login_required(login_url='login')
def answer_add(request, quiz_id, question_id):
    """
    Ajout d'une réponse à une question donnée.
    """
    if not hasattr(request.user, 'instructor'):
        return redirect('index_student')

    quiz = get_object_or_404(quiz_models.Quiz, id=quiz_id, owner=request.user)
    question = get_object_or_404(quiz_models.Question, id=question_id, quiz=quiz)

    if request.method == 'POST':
        text = request.POST.get('text')
        is_correct = request.POST.get('is_correct', 'false').lower() in ['true', 'on', '1']

        if text:
            quiz_models.Answer.objects.create(
                question=question,
                text=text,
                is_correct=is_correct
            )
        return redirect('answer_list', quiz_id=quiz.id, question_id=question.id)
    else:
        return render(request, 'pages/answer-add.html', {'quiz': quiz, 'question': question})

    


@login_required(login_url='login')
def answer_list(request, quiz_id, question_id):
    """
    Liste des réponses pour une question donnée.
    """
    if not hasattr(request.user, 'instructor'):
        return redirect('index_student')

    quiz = get_object_or_404(quiz_models.Quiz, id=quiz_id, owner=request.user)
    question = get_object_or_404(quiz_models.Question, id=question_id, quiz=quiz)
    answers = question.answers.all().order_by('id')

    context = {
        'quiz': quiz,
        'question': question,
        'answers': answers
    }
    return render(request, 'pages/question-edit-with-answers.html', context)


