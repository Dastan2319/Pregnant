from django.shortcuts import render
from django.http import HttpResponse
from .models import News
# Create your views here.

def index(request):
    d = {'foo':'test'}

    return render(request,'index.html',context=d)