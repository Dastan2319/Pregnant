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

import logging
logger = logging.getLogger(__name__)

def login_view(request):
    if request.user.is_authenticated:
        return redirect(views.index)

    if request.method == 'GET':
        return render(request,'login.html',context=dict(logForm=loginForm))
    if request.method == "POST":
        form = loginForm(request.POST)
        if not  form.is_valid():
            return render(request, 'login.html', context=dict( logForm=form))

        user = authenticate(request,username=form.cleaned_data['login'],password=form.cleaned_data['password'])
        if user is not None:
            login(request,user)
            logger.info('Зашел на сайт ' + str(user.username))
            return redirect(views.index)
        else:
            form.add_error('login','Логин или пароль не верный')
            logger.info('Пытался зайти на сайт ' + form.cleaned_data['login'])
            return render(request, 'login.html', context=dict(logForm=form))




def logout_view(request):
    logout(request)
    logger.info('Вышел сайта ' + str(request.user.username))
    return redirect(views.index)

