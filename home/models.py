from django.db import models
from django.db.models import fields as f
# Create your models here.

class News(models.Model):
    name = f.CharField(max_length=100 ,null=False)
    text = f.TextField(null=False)
    img = f.TextField()
    tags = f.TextField()
    date_add = f.DateTimeField(auto_now_add=True)

class Topic(models.Model):
    title = f.TextField(null=False)
    text = f.TextField(null=False)
    date_add = f.DateTimeField(auto_now_add=True)

class User(models.Model):
    name = f.CharField(max_length=100)
    password = f.CharField(max_length=20)
    isActive = True
    date_add = f.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    topic=models.ForeignKey(Topic,on_delete = models.CASCADE)

class Preparation(models.Model):
    title = f.CharField(max_length=100)
    description = f.TextField()

class NeededItems(models.Model):
    prepartion = models.ForeignKey(Preparation , on_delete=models.CASCADE)
    item = f.CharField(max_length=100)
    quantity = f.IntegerField()
    recommendationAddress = f.CharField(max_length=100) #типо рекламы

class MaternityHospital(models.Model):
    name = f.CharField(max_length=50)


class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    text = models.TextField(null=False)
    maternity_hospital = models.ForeignKey(MaternityHospital,on_delete = models.CASCADE)


