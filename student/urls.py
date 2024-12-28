from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('login', LoginView.as_view(template_name='school\learnplus\Learn\templates\pages\guest-login.html')),
    path('', views.index, name="index_student"), 
    # path('payment', views.payment, name='payment'),
    # path('subscription', views.subscription, name='subscription'), 
    # path('upgrade', views.upgrade, name='upgrade'),
    path('edit', views.edit, name='edit'),
    path('account_edit', views.account_edit, name='account-edit'),
    # path('invoice', views.invoice, name='invoice'),
    path('edit_basic', views.edit_basic, name='edit-basic'),
    path('edit_profile', views.edit_profile, name='edit-profile'),
    
    # path('browse_courses', views.browse_courses, name='browse-courses'),
    
    # path('earnings', views.earnings, name='earnings'),
    path('forum', views.forum, name='forum'),
    path('forum_lesson/<slug>', views.forum_lesson, name='forum-lesson'),
    path('forum_ask', views.forum_ask, name='forum-ask'),
    path('forum_thread/<slug>', views.forum_thread, name='forum-thread'),
    path('forum_thread/<slug>/reponse', views.post_forum_reponse, name='post_forum_reponse'),
    path('help_center', views.help_center, name='help-center'),
    path('messages/<str:classe>/', views.messages, name='messages'),
    path('my_courses', views.my_courses, name='my-courses'),
    path('quiz_list', views.quiz_list, name='quiz-list'),
    path('profile', views.profile, name='profile'),
    path('profile_posts', views.profile_posts, name='profile-posts'),
    path('take_quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
     path('quiz_result/<int:pk>/', views.quiz_result, name='quiz_result'),
    path('skip_question/<int:quiz_id>/<int:question_id>/', views.skip_question, name='skip_question'),
    
    path('take_course/<slug>', views.take_course, name='take-course'),
    path('take_quiz/<int:pk>/', views.take_quiz, name='take-quiz'),
    path('view_course', views.view_course, name='view-course'),
    path('login', LoginView.as_view(template_name='school\learnplus\Learn\templates\pages\guest-login.html')),


    ########## post ###############
    path('update_profil', views.update_profil, name='update_profil'),
    path('update_password', views.update_password, name='update_password'),
    path('post_forum', views.post_forum, name='post_forum'),
    path('post_forum_g', views.post_forum_g, name='post_forum_g'),

]