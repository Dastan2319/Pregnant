from django.db import models
from django.db.models import fields as f
# Create your models here.
from django.contrib.auth.models import User

class News(models.Model):
    name = f.CharField(max_length=100 ,null=False)
    text = f.TextField(null=False)
    img = f.TextField()
    tags = f.TextField()
    date_add = f.DateTimeField(auto_now_add=True)

# class User(models.Model):
#     name = f.CharField(max_length=100,null=False)
#     password = f.CharField(max_length=20,null=False)
#     isActive = True
#     date_add = f.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.name

# Topic это для форума название темы обсуждения
class Topic(models.Model):
    title = f.TextField(null=False)
    text = f.TextField(null=False)
    date_add = f.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class roles(models.Model):
    name = f.CharField(max_length=100)
    description = f.TextField(null=True)

    def __str__(self):
        return str(self.id)+' '+self.name
#
# class user_roles(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     roles = models.ForeignKey(roles, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.user.username) + ' имеет права ' + self.roles.name

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete = models.CASCADE)
    date_add = f.DateTimeField(auto_now_add=True)
    text = f.TextField()


class NeededItems(models.Model):
    title = f.CharField(max_length=100)
    quantity = f.IntegerField()
    recommendationAddress = f.CharField(max_length=100)  # типо рекламы


class Preparation(models.Model):
    name = f.CharField(max_length=100)
    description = f.TextField()



class PreparationList(models.Model):
    prepartion = models.ForeignKey(Preparation, on_delete=models.CASCADE)
    neededitems = models.ForeignKey(NeededItems, on_delete=models.CASCADE)

class MaternityHospital(models.Model):
    name = f.CharField(max_length=50)


class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    text = models.TextField(null=False)
    maternity_hospital = models.ForeignKey(MaternityHospital,on_delete = models.CASCADE)
