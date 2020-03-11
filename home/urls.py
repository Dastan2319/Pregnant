from django.urls import path
from home import views

urlpatterns = [
    path('', views.index),
    path('show/<int:id>',views.showNews)

]