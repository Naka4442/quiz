from django import forms

class Signupform(forms.Form):
    login = forms.CharField(max_length=24, label="", widget=forms.TextInput(attrs={"class" : "inp", "placeholder" : "Логин"}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class" : "inp", "placeholder" : "Почта"}))
    name = forms.CharField(max_length=24, label="", widget=forms.TextInput(attrs={"class" : "inp", "placeholder" : "Имя"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"class" : "inp", "placeholder" : "Пароль"}), label="")
    repeat_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"class" : "inp", "placeholder" : "Повторите пароль"}), label="")

class Signinform(forms.Form):
    login = forms.CharField(max_length=24, label="", widget=forms.TextInput(attrs={"class" : "inp", "placeholder" : "Логин"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"class" : "inp", "placeholder" : "Пароль"}), label="")

class Quizform(forms.Form):
    title = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={"class" : "inp", "placeholder" : "Название"}))
    image = forms.ImageField(label="Изображение")
