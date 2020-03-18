from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView
from .foms import NewsForm , registerForm,topicForm , commentForm , loginForm
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate ,login ,logout
from home import views
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request,'login.html',context=dict(logForm=loginForm))
        if request.method == "POST":
            form = loginForm(request.POST)
            if form.is_valid():
                user = authenticate(request,username=form.cleaned_data['login'],password=form.cleaned_data['password'])
                if user is not None:
                    login(request,user)
                    return redirect(views.index)
                else:
                    form.add_error('login','Логин или пароль не верный')
                    return render(request, 'login.html', context=dict(logForm=form))
            else:
                return render(request, 'login.html', context=dict( logForm=form))
    else:
        return redirect(views.index)

def logout_view(request):
    logout(request)
    return redirect(views.index)