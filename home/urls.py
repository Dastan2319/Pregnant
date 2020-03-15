from django.urls import path
from home import views

urlpatterns = [
    path('', views.index),
    path('reg',views.register),
    path('forum', views.forum)

]