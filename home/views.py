from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView

from .models import News


# Create your views here.

def index(request):
    # d = News.objects.getall()

    return render(request, 'index.html')


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
