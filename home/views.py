from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView
from .foms import NewsForm , registerForm,topicForm
from .models import News ,User, Topic

# Create your views here.

def index(request):
    if request.method == 'GET':
        myNews = News.objects.all()
        news=[]
        for item in myNews:
            news.append({"name":item.name,"text":item.text,"img":item.img,"tags":item.tags,"date_add":item.date_add})
        return render(request, 'index.html',context=dict(news=news))
    elif request.method == 'POST':
        form=NewsForm(request.POST)
        if form.is_valid():
            news=News(name=form.cleaned_data['name'],text=form.cleaned_data['text'],img=form.cleaned_data['img'],tags=form.cleaned_data['tags'])
            news.save()
            return redirect(index)
        else:
            myNews = News.objects.all()
            news = []
            for item in myNews:
                news.append({"name": item.name, "text": item.text, "img": item.img, "tags": item.tags,
                             "date_add": item.date_add})
            return render(request,'index.html',context=dict(news=news))

def register(request):
    if request.method == 'GET':
        return render(request,'register.html',context=dict(form=registerForm))
    elif request.method == 'POST':
        form=registerForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                findedUser = User.objects.filter(name=form.cleaned_data['name'])
                if findedUser:
                        form.add_error('name', "Пользователь уже существует")
                        return render(request, 'register.html', context=dict(form=form))
                else:
                    user = User(name=form.cleaned_data['name'],password=form.cleaned_data['password'])
                    user.save()
                    return redirect(index)
            else:
                # variables={'form':form}
                form.add_error('password', "Пароли не одинаковые")
                return render(request,'register.html',context=dict(form=form))
        else:
            return render(request, 'register.html', context=dict(form=form))

def forum(request):
    if request.method == "GET":
        temp = Topic.objects.all()
        topic = []
        for item in temp:
            topic.append(
                {"title": item.title, "text": item.text, "date_add": item.date_add})
        return render(request,'forum.html',context=dict(forum=topicForm,topic=topic))
    elif request.method == "POST":
        form=topicForm(request.POST)
        if form.is_valid():
            findedTopic=Topic.objects.all()

            addTopic=True
            for top in findedTopic:
                if(top.replace(' ','').lower()==form.cleaned_data['name']):
                    addTopic = False

            if addTopic == True:
                topic = Topic(name=form.cleaned_data['name'],text=form.cleaned_data['text'],user=1)
                # topic.save()
                return redirect(topic,topic.id)
            else:
                form.add_error('name', "Такая тему уже существует")
                return render(request, 'forum.html', context=dict(form=form))
        else:
            return render(request, 'forum.html', context=dict(form=form))


def topic(request):
    if request.method == 'GET':
        return render(request,'topic.html')




# def showNews(request, id: int):
#     addNews = News.objects.get(id=id)
#     return render(request, 'show.html', context=addNews)


# def CreateNews(request, text: str):
#     name, text, img, tags = text.split(':')
#     addNews = News(name=name, text=text, img=img, tags=tags)
#     addNews.save()
#     return redirect(index)

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
