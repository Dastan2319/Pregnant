from django import forms as f

class NewsForm(f.Form):
    name=f.CharField()
    text=f.CharField()
    img=f.CharField()
    tags=f.CharField()

class registerForm(f.Form):
    name = f.CharField(max_length=100,required=True)
    password = f.CharField(max_length=20,required=True)
    confirm_password = f.CharField(max_length=20,required=True)


class topicForm(f.Form):
    title = f.CharField(required=True)
    text = f.CharField(required=True)
