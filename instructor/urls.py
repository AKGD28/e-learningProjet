from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & Profile
    path('', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='instructor-profile'),
    path('account_edit', views.account_edit, name='instructor-account-edit'),

    # Courses / Chapitres
    path('course_add', views.course_add, name='course-add'),
    path('course_edit/<slug:slug>/', views.course_edit, name='course-edit'),
    path('courses', views.courses, name='instructor-courses'),
    path('matiere/<slug:slug>/', views.matiere, name='instructor-matiere'),

    # Lessons
    path('lesson-add/<slug:slug>/', views.lesson_add, name='instructor-lesson-add'),
    path('lesson-edit/<int:id>/<slug:slug>/', views.lesson_edit, name='instructor-lesson-edit'),

    # Forum
    path('forum', views.forum, name='instructor-forum'),
    path('forum_ask', views.forum_ask, name='instructor-forum-ask'),
    path('forum_thread/<slug:slug>/', views.forum_thread, name='instructor-forum-thread'),

    # Messages (chat)
    path('messages/<str:classe>/', views.messages, name='instructor-messages'),

    # Quiz Management
    path('quizzes', views.quizzes, name='instructor-quizzes'),
    path('quiz_add', views.quiz_add, name='instructor-quiz-add'),
    path('quiz_edit/<int:quiz_id>/', views.quiz_edit, name='instructor-quiz-edit'),
    path('review_quiz/<int:quiz_id>/', views.review_quiz, name='instructor-review-quiz'),

    # ----- GESTION DES QUESTIONS -----
    path('quiz/<int:quiz_id>/questions/', 
         views.quiz_edit_questions, 
         name='quiz_edit_questions'),
    path('quiz/<int:quiz_id>/question/add/', 
         views.question_add, 
         name='question_add'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/edit/', 
         views.question_edit, 
         name='question_edit'),
    path('question/delete/', 
         views.question_delete, 
         name='question_delete'),
    path('quiz/<int:quiz_id>/results/', 
         views.quiz_results, 
         name='quiz_results'),

    # ----- GESTION DES RÉPONSES -----
    path('quiz/<int:quiz_id>/question/<int:question_id>/answers/', 
         views.answer_list, 
         name='answer_list'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/answer/add/', 
         views.answer_add, 
         name='answer_add'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/answer/<int:answer_id>/edit/', 
         views.answer_edit, 
         name='answer_edit'),
    path('answer/delete/', 
         views.answer_delete, 
         name='answer_delete'),

    # POST / AJAX
    path('post_cours', views.post_cours, name='post_cours'),
    path('delete_chapitre', views.delete_chapitre, name='delete_chapitre'),
    path('delete_lesson', views.delete_lesson, name='delete_lesson'),
    path('post_lesson', views.post_lesson, name='post_lesson'),

    # Update profil & password
    path('update_profil', views.update_profil, name='update_profil'),
    path('update_password', views.update_password, name='update_password'),

    # Forum post
    path('post_forum', views.post_forum, name='instructor_post_forum'),
]
