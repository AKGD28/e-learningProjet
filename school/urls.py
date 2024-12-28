from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('signup', views.signup, name="guests_signup"),
    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('post', views.islogin, name="post"),
    path('deconnexion', views.deconnexion, name="deconnexion"),
]