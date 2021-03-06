from django import forms as f


class NewsForm(f.Form):
    name = f.CharField()
    text = f.CharField()
    img = f.CharField()
    tags = f.CharField()


class registerForm(f.Form):
    name = f.CharField(max_length=100, required=True)
    password = f.CharField(max_length=20, min_length=4, required=True)
    confirm_password = f.CharField(max_length=20, min_length=4, required=True)


class topicForm(f.Form):
    title = f.CharField(required=True)
    text = f.CharField(required=True, widget=f.Textarea)


class commentForm(f.Form):
    text = f.CharField(required=True, widget=f.TextInput(attrs={'class': 'inputForm'}))


class loginForm(f.Form):
    login = f.CharField(required=True)
    password = f.CharField(required=True)


class NeedItemsForm(f.Form):
    title = f.CharField(max_length=100)
    quantity = f.IntegerField()
    recommendationAddress = f.CharField(max_length=100)


class PreparationForm(f.Form):
    name = f.CharField(max_length=100)
    description = f.CharField()


class HospitalForm(f.Form):
    name = f.CharField(max_length=50, required=True)


class UserForm(f.Form):
    password = f.CharField(max_length=20, min_length=4, required=False)
    first_name = f.CharField(max_length=50, required=True)
    last_name = f.CharField(max_length=50, required=True)
    email = f.EmailField(max_length=100, required=True)

class watchUserForm(f.Form):
    first_name = f.CharField( widget=f.TextInput(attrs={'disabled': 'true'}))
    last_name = f.CharField( widget=f.TextInput(attrs={'disabled': 'true'}))
    email = f.EmailField( widget=f.TextInput(attrs={'disabled': 'true'}))
