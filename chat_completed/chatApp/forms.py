from django.forms import forms, ModelForm, PasswordInput, CharField, TextInput, Form

from chatApp.models import ChatUser
from chatApp.validators import  email_validation


class RegistrationForm(ModelForm):
    class Meta:
        model = ChatUser

        fields = ["name", "login", "password"]
        widgets = {"password":PasswordInput()}

    def clean_login(self):
        user_name = self.cleaned_data["login"]
        email_validation(user_name)
        return self.cleaned_data["login"]

class LoginForm(Form):
    login = CharField(max_length=100)
    password = CharField(max_length=100, widget=PasswordInput)
    def clean_login(self):
        user_name = self.cleaned_data["login"]
        email_validation(user_name)
        return self.cleaned_data["login"]