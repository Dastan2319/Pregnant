from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView
from .foms import NewsForm, registerForm, topicForm, commentForm, loginForm, NeedItemsForm, PreparationForm, \
    HospitalForm, UserForm, watchUserForm
from .models import News, Topic, Comments, Preparation, NeededItems, PreparationList, MaternityHospital, Feedback
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login

def index(request):
    if request.method == 'GET':
        myNews = News.objects.all()
        news = []
        for item in myNews:
            news.append(
                {"name": item.name, "text": item.text, "img": item.img, "tags": item.tags, "date_add": item.date_add})
        cont = {}
        if request.user.is_authenticated:
            isAdmin = 'false'
            if request.user.has_perms('home.add_news', 'home.change_news'):
                isAdmin = 'true'
            cont = {'news': news, 'islogged': 'true','username':dict(user= request.user.username,id=request.user.id), 'isAdmin': isAdmin}
        else:
            cont = {'news': news, 'islogged': 'false', 'logForm': loginForm, 'isAdmin': 'false'}
        return render(request, 'index.html', context=cont)
    elif request.method == 'POST':
        if request.user.has_perm('home.add_news'):
            form = NewsForm(request.POST)
            if form.is_valid():
                news = News(name=form.cleaned_data['name'], text=form.cleaned_data['text'],
                            img=form.cleaned_data['img'], tags=form.cleaned_data['tags'])
                news.save()
                return redirect(index)
            else:
                myNews = News.objects.all()
                news = []
                for item in myNews:
                    news.append({"name": item.name, "text": item.text, "img": item.img, "tags": item.tags,
                                 "date_add": item.date_add})
                return render(request, 'index.html', context=dict(news=news, logForm=loginForm))


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'register.html', context=dict(form=registerForm))
        elif request.method == 'POST':
            form = registerForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                    findedUser = User.objects.filter(username=form.cleaned_data['name'])
                    if findedUser:
                        form.add_error('name', "Пользователь уже существует")
                        return render(request, 'register.html', context=dict(form=form))
                    else:
                        my_group = Group.objects.get(name='User')
                        user = User.objects.create_user(form.cleaned_data['name'], '', form.cleaned_data['password'])
                        user.save()
                        my_group.user_set.add(user)
                        return redirect(index)
                else:
                    # variables={'form':form}
                    form.add_error('password', "Пароли не одинаковые")
                    return render(request, 'register.html', context=dict(form=form))
            else:
                return render(request, 'register.html', context=dict(form=form))
    else:
        return redirect(index)


def forum(request):
    # isAdmin = 'false'
    # isLogged = 'false'
    # username = ''
    # if request.user.is_authenticated:
    #     if request.user.has_perms('home.add_topic', 'home.change_topic'):
    #         isAdmin = 'true'
    #     isLogged = 'true'
    #     username = request.user.username

    auth = getAuth(request, 'topic')
    isAdmin = auth['isAdmin']
    isLogged = auth['isLogged']
    username = auth['username']

    if request.method == "GET":
        temp = Topic.objects.all()
        topic = []
        for item in temp:
            topic.append(
                {"id": item.id, "title": item.title, "text": item.text, "date_add": item.date_add})

        return render(request, 'forum.html',
                      context=dict(forum=topicForm, topic=topic, dialog='false', isAdmin=isAdmin, islogged=isLogged,
                                   username=username))
    elif request.method == "POST":
        if request.user.has_perm('home.add_topic'):
            form = topicForm(request.POST)
            if form.is_valid():
                findedTopic = Topic.objects.all()

                addTopic = True
                for top in findedTopic:
                    if top.title.replace(' ', '').lower() == form.cleaned_data['title'].replace(' ', '').lower():
                        addTopic = False

                if addTopic == True:
                    newtopic = Topic(title=form.cleaned_data['title'], text=form.cleaned_data['text'],
                                     user=request.user)
                    newtopic.save()
                    return redirect('/home/topic/' + str(newtopic.id))
                else:
                    temp = Topic.objects.all()
                    topic = []
                    for item in temp:
                        topic.append(
                            {"id": item.id, "title": item.title, "text": item.text, "date_add": item.date_add})

                    form.add_error('title', "Такая тему уже существует")
                    return render(request, 'forum.html',
                                  context=dict(forum=form, topic=topic, dialog='true', isAdmin=isAdmin,
                                               islogged=isLogged, username=username))
            else:
                temp = Topic.objects.all()
                topic = []
                for item in temp:
                    topic.append(
                        {"id": item.id, "title": item.title, "text": item.text, "date_add": item.date_add})
                return render(request, 'forum.html',
                              context=dict(forum=form, topic=topic, dialog='true', isAdmin=isAdmin, islogged=isLogged,
                                           username=username))
        else:
            return redirect(forum)


def topic(request, id):
    auth = getAuth(request, 'topic')
    isAdmin = auth['isAdmin']
    isLogged = auth['isLogged']
    username = auth['username']

    topic = Topic.objects.get(id=id)
    comments = Comments.objects.filter(topic=id)
    dictComment = []
    for comm in comments:
        dictComment.append({'name': comm.user.username, 'comment': comm.text, "date_add": comm.date_add})

    if request.method == 'GET':
        return render(request, 'topic.html',
                      context=dict(topic=topic, comment=dictComment, form=commentForm, isAdmin=isAdmin,
                                   islogged=isLogged, username=username))
    elif request.method == 'POST':
        if request.user.has_perm('home.add_comments'):
            form = commentForm(request.POST)
            if form.is_valid():
                this_topic = Topic.objects.get(id=id)
                comment = Comments(user=request.user, topic=this_topic, text=form.cleaned_data['text'])
                comment.save()
                return redirect(topic, id)
            else:
                return render(request, 'topic.html',
                              context=dict(topic=topic, comment=dictComment, form=form, isAdmin=isAdmin,
                                           islogged=isLogged, username=username))


def preparation(request):
    auth = getAuth(request, 'preparation')
    isAdmin = auth['isAdmin']
    isLogged = auth['isLogged']
    username = auth['username']

    needItems = Preparation.objects.all()
    if request.method == 'GET':

        return render(request, 'preparation.html',
                      context=dict(needItems=needItems, needForm=PreparationForm, isAdmin=isAdmin, islogged=isLogged,
                                   username=username))
    elif request.method == 'POST':
        if request.user.has_perm('add_preparation'):
            form = PreparationForm(request.POST)
            if form.is_valid():
                need = NeededItems(title=form.cleaned_data['title'], quantity=int(form.cleaned_data['quantity']),
                                   recommendationAddress=form.cleaned_data['recommendationAddress'])
                need.save()
                return redirect(needitems, need.id)
            else:
                return render(request, 'preparation.html',
                              context=dict(needItems=needItems, needForm=form, isAdmin=isAdmin,
                                           islogged=isLogged, username=username))


def needitems(request, id):
    auth = getAuth(request, 'preparation')
    isAdmin = auth['isAdmin']
    isLogged = auth['isLogged']
    username = auth['username']

    prepar = Preparation.objects.get(id=id)
    list = PreparationList.objects.filter(prepartion=prepar)
    thisItems = []
    for i in list:
        thisItems.append({'title': i.neededitems.title, 'quantity': i.neededitems.quantity,
                          'recommendationAddress': i.neededitems.recommendationAddress})

    if request.method == 'GET':
        return render(request, 'needitems.html',
                      context=dict(list=thisItems, prepar=prepar, form=NeedItemsForm, isAdmin=isAdmin,
                                   islogged=isLogged, username=username))
    if request.method == 'POST':
        if request.user.has_perm('home.add_preparation'):
            form = NeedItemsForm(request.POST)
            if form.is_valid():
                newNeed = NeededItems(title=form.cleaned_data['title'], quantity=form.cleaned_data['quantity'],
                                      recommendationAddress=form.cleaned_data['recommendationAddress'])
                newNeed.save()
                newList = PreparationList(prepartion=prepar, neededitems=newNeed)
                newList.save()
                return redirect(needitems, id)
            else:
                return render(request, 'needitems.html',
                              context=dict(list=thisItems, prepar=prepar, form=form, isAdmin=isAdmin,
                                           islogged=isLogged, username=username))


def materHospit(request):
    auth = getAuth(request, 'maternityhospital')
    isAdmin = auth['isAdmin']
    isLogged = auth['isLogged']
    username = auth['username']

    hospitals = MaternityHospital.objects.all()
    if request.method == 'GET':
        return render(request, 'MaternityHospital.html',
                      context=dict(hospitals=hospitals, form=HospitalForm, isAdmin=isAdmin, islogged=isLogged,
                                   username=username, open='false'))
    elif request.method == 'POST':
        if request.user.has_perm('add_maternityhospital'):
            form = HospitalForm(request.POST)
            if form.is_valid():
                hospital = MaternityHospital.objects.filter(name=form.cleaned_data['name'])
                if not hospital:
                    need = MaternityHospital(name=form.cleaned_data['name'])
                    need.save()
                    return redirect(materHospit)
                else:
                    form.add_error('name', 'Такой список уже существует')
                    return render(request, 'MaternityHospital.html',
                                  context=dict(hospitals=hospitals, form=form, isAdmin=isAdmin,
                                               islogged=isLogged, username=username, open='true'))
            else:
                return render(request, 'MaternityHospital.html',
                              context=dict(hospitals=hospitals, form=form, isAdmin=isAdmin,
                                           islogged=isLogged, username=username, open='false'))


def hospital(request, id):
    auth = getAuth(request, 'maternityhospital')
    isAdmin = auth['isAdmin']
    isLogged = auth['isLogged']
    username = auth['username']

    Hospital = MaternityHospital.objects.get(id=id)
    comments = Feedback.objects.filter(maternity_hospital=id)
    if request.method == 'GET':
        return render(request, 'hospital.html',
                      context=dict(hospitals=Hospital, comments=comments, form=commentForm, isAdmin=isAdmin,
                                   islogged=isLogged, username=username, open='false'))
    elif request.method == 'POST':
        if request.user.is_authenticated:
            form = commentForm(request.POST)
            if form.is_valid():
                need = Feedback(user=request.user, text=form.cleaned_data['text'], maternity_hospital=Hospital)
                need.save()
                return redirect(hospital, id)
            else:
                return render(request, 'hospital.html',
                              context=dict(hospitals=Hospital, comments=comments, form=form, isAdmin=isAdmin,
                                           islogged=isLogged, username=username))


@login_required
def profile(request, id):
    isAdmin = 'true'
    isLogged = 'true'
    username = dict(user=request.user.username,id=request.user.id)


    if request.method == 'GET':
        if request.user.id == id:
            form = UserForm({'first_name':request.user.first_name,'last_name': request.user.last_name,'email':request.user.email})
            return render(request, 'profile.html', context=dict(isAdmin=isAdmin,isProfile='true', form=form,isLogged=isLogged,username=username))
        else:
            user=User.objects.get(id=id)
            form = watchUserForm({'first_name':user.first_name,'last_name': user.last_name,'email':user.email})
            return render(request, 'profile.html', context=dict(isAdmin=isAdmin,isProfile='false' ,form=form,isLogged=isLogged,username=username))
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.id == id:
                form = UserForm(request.POST)
                if form.is_valid():
                    user = User.objects.get(id=id)
                    if form.cleaned_data['password'] != '':
                        user.set_password(form.cleaned_data['password'])
                        authUser = authenticate(request, username=user.username,
                                            password=user.password)
                        if authUser is not None:
                            login(request, authUser)
                            return redirect(profile, user.id)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.email = form.cleaned_data['email']
                    user.save()
                    return redirect(profile,user.id)



def getAuth(request, modelName):
    isAdmin = 'false'
    isLogged = 'false'
    username = ''
    if request.user.is_authenticated:
        if request.user.has_perms(f'home.add_{modelName}', f'home.change_{modelName}'):
            isAdmin = 'true'
        isLogged = 'true'
        username = dict(user=request.user.username,id=request.user.id)
    return dict(isAdmin=isAdmin, isLogged=isLogged, username=username)

#
# def UpdateNews(request, id: int, text: str):
#     name, text, img, tags = text.split(':')
#     addNews = News.objects.get(id=id)
#     addNews.name = name
#     addNews.text = text
#     addNews.img = img
#     addNews.tags = tags
#     addNews.save()
#     return redirect(index)

#
# def DeleteNews(request, id: int):
#     delNews = News.objects.filter(id=id).delete()
#     return redirect(index)
