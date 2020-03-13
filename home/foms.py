from django import forms as f

class NewsForm(f.Form):
    name=f.CharField()
    text=f.CharField()
    img=f.CharField()
    tags=f.CharField()