from django.shortcuts import render
from django.contrib.auth import authenticate, login as login_request, logout
from django.shortcuts import render , redirect 
import json
from django.http import JsonResponse
from django.contrib.auth.models import User 

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login(request):
    if request.user.is_authenticated:
        # Redirection si l'utilisateur est connecté
        if hasattr(request.user, 'student_user'):
            return redirect('index_student')
        elif hasattr(request.user, 'instructor'):
            return redirect('dashboard')
        else:
            return redirect('/admin/')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if hasattr(user, 'student_user'):
                    return redirect('index_student')
                elif hasattr(user, 'instructor'):
                    return redirect('dashboard')
                else:
                    return redirect('/admin/')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()
    
    return render(request, 'pages/guest-login.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.student_user:
                    return redirect('index_student')
            except:
                print("2")
                if request.user.instructor:
                    return redirect('dashboard')
        except:
            print("3")
            return redirect("/admin/")
    else:

        datas = {

        }
        return render(request, 'pages/guest-signup.html', datas) 

def forgot_password(request):
    if request.user.is_authenticated:
        try:
            try:
                print("1")
                if request.user.student_user:
                    return redirect('index_student')
            except:
                print("2")
                if request.user.instructor:
                    return redirect('dashboard')
        except:
            print("3")
            return redirect("/admin/")
    else:
        datas = {

        }
        return render(request, 'pages/guest-forgot-password.html', datas)



def islogin(request):

    postdata = json.loads(request.body.decode('utf-8'))
        
    # name = postdata['name']

    username = postdata['username']
    password = postdata['password']

    isSuccess = False
    u_type = ''
    try:
        
        if '@' in username:
            user = authenticate(email=username, password=password)
            utilisateur = User.objects.get(email=username)
            print(username)
        else:
            user = authenticate(username=username, password=password)
            utilisateur = User.objects.get(username=username)
            
        if user is not None and user.is_active:
            print("user is login")
            isSuccess = True
            login_request(request, user)
            try:
                try:
                    print("1")
                    if utilisateur.student_user:
                        u_type = "student"
                except:
                    print("2")
                    if utilisateur.instructor:
                        u_type = "instructor"
            except:
                print("3")
                u_type = "admin"

            datas = {
                'redirect' : u_type,
                'success':True,
                'message':'Vous êtes connectés!!!',
            }
            return JsonResponse(datas,safe=False) # page si connect
                
        else:
            data = {
                'success':False,
                'message':'Vos identifiants ne sont pas correcte',
            }
            return JsonResponse(data, safe=False)
    except:
        data = {
            'success':False,
            'message':"Une erreur s'est produite",
        }
        return JsonResponse(data, safe=False)
    
def deconnexion(request):
    logout(request)
    return redirect('login')
