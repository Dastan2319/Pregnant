from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView
from .foms import NewsForm
from .models import News


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



def showNews(request, id: int):
    addNews = News.objects.get(id=id)
    return render(request, 'show.html', context=addNews)


def CreateNews(request, text: str):
    name, text, img, tags = text.split(':')
    addNews = News(name=name, text=text, img=img, tags=tags)
    addNews.save()
    return redirect(index)


def UpdateNews(request, id: int, text: str):
    name, text, img, tags = text.split(':')
    addNews = News.objects.get(id=id)
    addNews.name = name
    addNews.text = text
    addNews.img = img
    addNews.tags = tags
    addNews.save()
    return redirect(index)


def DeleteNews(request, id: int):
    delNews = News.objects.filter(id=id).delete()
    return redirect(index)
