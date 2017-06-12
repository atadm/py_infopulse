from django.core.exceptions import ValidationError

from chatApp.models import ChatUser

class UserService:
    instance = None
    def __new__(cls, *args, **kwargs):
        if UserService.instance == None:
            UserService.instance = object.__new__(cls)
        return UserService.instance
    def save_user(self,form_data):
        #code from views.py
        chat_users = ChatUser(name=form_data.cleaned_data["name"],
                              login=form_data.cleaned_data["login"],
                              password=form_data.cleaned_data["password"],
                              role_id_id=1)
        chat_users.save()

    def verify_login(self,form_data):
        chat_users = ChatUser.objects.filter(login=form_data
                                             .cleaned_data["login"]).first()
        if chat_users == None:
            return None
        if chat_users.password != form_data.cleaned_data["password"]:
            return None
        return chat_users