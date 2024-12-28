from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from school import models as school_models
from forum import models as forum_models
from instructor import models as instructor_models
from django.db.models import Q
from chat import models as chat_models
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.db import transaction
import json
from django.http import JsonResponse 
from quiz.models import Quiz, Question, Answer, StudentAnswer, TakenQuiz
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from forum.models import  Reponse  # Adaptez selon vos modèles


# Create your views here.
@login_required(login_url = 'login')
def index(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard') 
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    cours = school_models.Cours.objects.filter(Q(status=True) & Q(chapitre__classe=request.user.student_user.classe)).order_by('-date_add')[:5]
                    forum = forum_models.Sujet.objects.filter(cours__chapitre__classe=request.user.student_user.classe)[:5]
                    forum_count = forum_models.Sujet.objects.filter(cours__chapitre__classe=request.user.student_user.classe).count()
                    datas = {
                                'cours': cours,
                                'forum': forum,
                                'forum_count': forum_count,
                           }
                return render(request,'pages/fixed-student-dashboard.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")



 


@login_required(login_url = 'login')
def edit(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-account-edit.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")

@login_required(login_url = 'login')
def edit_basic(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-account-edit-basic.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")

@login_required(login_url = 'login')
def edit_profile(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-account-edit-profile.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")


 


@login_required(login_url = 'login')
def courses(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard') 
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                   
                    datas = {
                                
                           }
                return render(request,'pages/fixed-student-courses.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    



@login_required(login_url = 'login')
def forum(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    forum_general = forum_models.Sujet.objects.filter(cours=None)
                    forum = forum_models.Sujet.objects.filter(cours__chapitre__classe=request.user.student_user.classe)
                    datas = {
                        'forum_general': forum_general,
                        'forum': forum,
                    }
                return render(request,'pages/fixed-student-forum.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")





@login_required(login_url = 'login')
def forum_lesson(request, slug):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    lesson = school_models.Cours.objects.get(slug=slug)
                    datas = {
                        'lesson':lesson,
                    }
                return render(request,'pages/fixed-student-forum-lesson.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")



@login_required(login_url = 'login')
def forum_ask(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-forum-ask.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")




@login_required(login_url = 'login')
def forum_thread(request, slug):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    forum = forum_models.Sujet.objects.get(slug=slug)
                    datas = {
                        "forum": forum,
                    }
                return render(request,'pages/fixed-student-forum-thread.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    

@login_required(login_url = 'login')
def help_center(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-help-center.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    

@login_required(login_url = 'login')
def messages(request, classe):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    exist_classe = chat_models.Salon.objects.get(classe=request.user.student_user.classe)
                    info = school_models.Classe.objects.get(id=request.user.student_user.classe.id)
                    instructor = instructor_models.Instructor.objects.get(classe__id=request.user.student_user.classe.id)
                    user_room = ''                    
                    print(user_room)
                    datas = {
                        'instructor':instructor,
                        'info_classe':info,
                        'classe': exist_classe,
                        'classe_json': mark_safe(json.dumps(exist_classe.id)),
                        'username': mark_safe(json.dumps(request.user.username))
                    }
                return render(request,'pages/fixed-student-messages.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    
# @login_required(login_url = 'login')
# def messages_2(request):
#     if request.user.is_authenticated:
#         try:
#             try:
#                 print("1")
#                 if request.user.instructor:
#                     return redirect('dashboard')
#             except Exception as e:
#                 print(e)
#                 print("2")
#                 if request.user.student_user:
#                     datas = {

#                            }
#                 return render(request,'pages/fixed-student-messages-2.html',datas)
#         except Exception as e:
#             print(e)
#             print("3")
#             return redirect("/admin/")

@login_required(login_url = 'login')
def my_courses(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    chapitre = school_models.Chapitre.objects.filter(status=True)
                    cours = school_models.Cours.objects.filter(status=True)
                    all_cours = school_models.Cours.objects.filter(Q(status=True) & Q(chapitre__classe=request.user.student_user.classe))
                    datas = {
                                'chapitre':chapitre, 
                                'cours':cours,
                                'all_cours': all_cours,
                           }
                return render(request,'pages/fixed-student-my-courses.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")

@login_required(login_url='login')
def quiz_list(request):
    # Rediriger les instructeurs vers le tableau de bord
    if hasattr(request.user, 'instructor'):
        return redirect('dashboard')
    
    # Vérifier si l'utilisateur est un étudiant
    if hasattr(request.user, 'student_user'):
        student = request.user.student_user
        quizzes = student.classe.quizzes.filter(status=True)  # Récupérer les quizzes de la classe de l'étudiant
        
        # Ajouter une vérification pour savoir si un quiz a déjà été pris
        quizzes_with_status = []
        for quiz in quizzes:
            taken_quiz = quiz.taken_quizzes.filter(student=student).first()
            has_taken = taken_quiz is not None
            quizzes_with_status.append({
                'quiz': quiz,
                'has_taken': has_taken,
                'result_url': reverse('quiz_result', args=[quiz.id]) if has_taken else None  # URL des résultats si pris
            })
        
        datas = {
            'quizzes': quizzes_with_status,  # Liste des quizzes avec leur statut et URL des résultats
        }
        return render(request, 'pages/fixed-student-quiz-list.html', datas)
    
    # Si aucune condition n'est remplie, redirigez vers l'administration
    return redirect('/admin/')





@login_required(login_url = 'login')
def profile(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-profile.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")

@login_required(login_url = 'login')
def profile_posts(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-profile-posts.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    

@login_required(login_url='login')
def quiz_result(request, pk):
    user = request.user

    # Vérification que l'utilisateur est un étudiant
    if not hasattr(user, 'student_user'):
        return redirect('dashboard')

    student = user.student_user
    quiz = get_object_or_404(Quiz, pk=pk)
    taken_quiz = get_object_or_404(TakenQuiz, student=student, quiz=quiz)

    # Préparer les données des questions et réponses
    questions = quiz.questions.all()
    question_results = []
    for question in questions:
        student_answer = student.quiz_answers.filter(answer__question=question).first()
        is_correct = student_answer.answer.is_correct if student_answer else False
        question_results.append({
            'text': question.text,
            'is_correct': is_correct
        })

    return render(request, 'pages/fixed-student-quiz-results.html', {
        'quiz': quiz,
        'taken_quiz': taken_quiz,
        'score': taken_quiz.score,
        'percentage': taken_quiz.percentage,
        'question_results': question_results,  # Passer les résultats des questions au template
    })


@login_required(login_url = 'login')
def statement(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-statement.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    

# @login_required(login_url = 'login')
# def student_take_course(request, slug):
#     if request.user.is_authenticated:
#         try:
#             try:
#                 print("1")
#                 if request.user.instructor:
#                     return redirect('dashboard')
#             except Exception as e:
#                 print(e)
#                 print("2")
#                 if request.user.student_user:
#                     cours  = school_models.Cours.objets.get(slug=slug)
#                     datas = {
#                         'cours': cours,
#                     }
#                 return render(request,'pages/fixed-student-student-take-course.html',datas)
#         except Exception as e:
#             print(e)
#             print("3")
#             return redirect("/admin/")


@login_required(login_url='login')
def take_course(request, slug):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    cours = school_models.Cours.objects.get(slug=slug)
                    instructor = instructor_models.Instructor.objects.get(classe__id=request.user.student_user.classe.id)
                    datas = {
                        'cours': cours,
                        'instructor' : instructor,
                    }
                return render(request,'pages/fixed-student-take-course.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect('my-courses')



@login_required(login_url='login')
def skip_question(request, quiz_id, question_id):
    user = request.user

    # Vérifier que l'utilisateur est un étudiant
    if not hasattr(user, 'student_user'):
        return redirect('dashboard')

    student = user.student_user
    quiz = get_object_or_404(Quiz, id=quiz_id, status=True)

    # Vérifier si le quiz a déjà été pris
    if TakenQuiz.objects.filter(student=student, quiz=quiz).exists():
        return redirect('dashboard')  # Ou afficher un message indiquant que le quiz est terminé

    # Logique pour passer à la prochaine question
    # Ici, on redirige simplement vers la vue `take_quiz` pour continuer
    return redirect('take_quiz', pk=quiz_id)
   

@login_required(login_url='login')
def take_quiz(request, pk):
    user = request.user

    # Vérification que l'utilisateur est un étudiant
    if not hasattr(user, 'student_user'):
        return redirect('dashboard')

    student = user.student_user
    quiz = get_object_or_404(Quiz, pk=pk, status=True)

    # Vérification si le quiz a déjà été pris
    if TakenQuiz.objects.filter(student=student, quiz=quiz).exists():
        return redirect('dashboard')  # Ou affichez un message indiquant que le quiz a déjà été complété

    # Initialiser les variables pour le template
    total_questions = quiz.questions.count()
    answered_questions = student.quiz_answers.filter(answer__question__quiz=quiz).values('answer__question').distinct().count()
    left_questions = total_questions - answered_questions
    progress_percentage = (answered_questions / total_questions) * 100 if total_questions > 0 else 0

    # Générer les numéros des questions restantes
    pending_question_numbers = range(answered_questions + 1, total_questions + 1)

    # Si une soumission est reçue
    if request.method == 'POST':
        with transaction.atomic():
            correct_answers = 0

            for question in quiz.questions.all():
                selected_answer_id = request.POST.get(str(question.id))
                if selected_answer_id:
                    selected_answer = get_object_or_404(Answer, id=selected_answer_id)

                    # Enregistrer la réponse de l'étudiant
                    StudentAnswer.objects.create(student=student, answer=selected_answer)

                    # Vérifier si la réponse est correcte
                    if selected_answer.is_correct:
                        correct_answers += 1

            # Calculer le score et enregistrer dans TakenQuiz
            percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            TakenQuiz.objects.create(
                student=student,
                quiz=quiz,
                score=correct_answers,
                percentage=percentage,
                date=now()
            )

        # Rediriger après la soumission
        return redirect('quiz_result', pk=quiz.pk)

    # Récupérer la prochaine question non répondue
    unanswered_questions = quiz.questions.exclude(
        pk__in=student.quiz_answers.filter(answer__question__quiz=quiz).values_list('answer__question__pk', flat=True)
    ).order_by('id')

    if unanswered_questions.exists():
        current_question = unanswered_questions.first()
        current_question_number = answered_questions + 1
    else:
        current_question = None
        current_question_number = None

    # Afficher les questions pour résoudre le quiz
    questions = quiz.questions.prefetch_related('answers')
    return render(request, 'pages/fixed-student-take-quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'total_questions': total_questions,
        'answered_questions': answered_questions,
        'left_questions': left_questions,
        'progress_percentage': progress_percentage,
        'current_question': current_question,
        'current_question_number': current_question_number,  # Ajouté
        'pending_question_numbers': pending_question_numbers,  # Ajouté
    })
@login_required(login_url = 'login')
def view_course(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-view-course.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")
    
@login_required(login_url = 'login')
def account_edit(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.instructor:
                    return redirect('dashboard')
            except Exception as e:
                print(e)
                print("2")
                if request.user.student_user:
                    datas = {

                           }
                return render(request,'pages/fixed-student-account-edit.html',datas)
        except Exception as e:
            print(e)
            print("3")
            return redirect("/admin/")

        
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
        student = models.Student.objects.get(user__id=request.user.id)
        student.bio = bio
        student.save()
        try:
            image = request.FILES["file"]
            student.photo = image 
            student.save()

        except:
            pass
        success = True 
        message = "vos informations ont été modifié avec succés"

    except:
        success = False
        message = "une erreur est subvenue lors de la mise à jour"
    data = {
        "success" : success,
        "message" : message,
        }
    return JsonResponse(data,safe=False)

        
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
            message = "Les mots de passe ne sont pas identiques"
        else:
            user = User.objects.get(username=request.user.username)
            username = user.username
            user.password = new_password
            user.set_password(user.password)
            user.save()
            user = authenticate(username=username, password=new_password)
            login(request, user)
            success = True 
            message = "Mot de passe modfifié avec succès"
    except Exception as e:
        print(e)
        success = False
        message = "une erreur est subvenue lors de la mise à jour"
    data = {
        "success" : success,
        "message" : message,
        }
    return JsonResponse(data,safe=False)

    

        
def post_forum(request):
    titre = request.POST.get("titre")
    question = request.POST.get("question")
    lesson = request.POST.get("lesson")
    val = ""
    try:
        lesson = school_models.Cours.objects.get(id=int(lesson))
        forum = forum_models.Sujet()
        forum.titre = titre
        forum.question = question
        forum.cours = lesson
        forum.user = request.user
        forum.save()
        val = forum.slug
        success = True 
        message = "Votre sujet a bien été ajouté!"
    except Exception as e:
        print(e)
        success = False
        message = "une erreur est subvenue lors de la soumission"
    data = {
        "success" : success,
        "message": message,
        "forum": val,
        }
    return JsonResponse(data,safe=False)

    
def post_forum_g(request):
    titre = request.POST.get("titre")
    question = request.POST.get("question")
    val = ""
    try:
        forum = forum_models.Sujet()
        forum.titre = titre
        forum.question = question
        forum.user = request.user
        forum.save()
        val = forum.slug
        success = True 
        message = "Votre sujet a bien été ajouté!"
    except Exception as e:
        print(e)
        success = False
        message = "une erreur est subvenue lors de la soumission"
    data = {
        "success" : success,
        "message": message,
        "forum": val,
        }
    return JsonResponse(data,safe=False)

@login_required
@csrf_exempt  # ou configurez la protection CSRF correctement
def post_forum_reponse(request, slug):
    if request.method == 'POST':
        reponse_content = request.POST.get('reponse', '').strip()
        try:
            sujet = forum_models.Sujet.objects.get(slug=slug)
        except forum_models.Sujet.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Le sujet est introuvable.'
            })

        if not reponse_content:
            return JsonResponse({
                'success': False,
                'message': 'Le contenu de la réponse est vide.'
            })

        forum_models.Reponse.objects.create(
            sujet=sujet,
            user=request.user,
            reponse=reponse_content
        )

        return JsonResponse({
            'success': True,
            'message': 'Votre réponse a été publiée avec succès.'
        })

    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée.'
    })
