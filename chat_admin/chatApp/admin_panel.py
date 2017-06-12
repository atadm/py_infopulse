
from rest_framework.decorators import api_view

from chatApp.models import ChatUser, Ban


@api_view(["GET"])
def get_all_users(request):
    if request.session.get("login") != None and request.session.get("admin") == True:
        all_users = ChatUser.objects.filter(role_id__role_name = "user")
        json_users = {"users":[]}
        for user in all_users:
            b = Ban.objects.filter(user_id = user)

