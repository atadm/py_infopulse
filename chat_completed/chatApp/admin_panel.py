# from django.core.serializers
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from chatApp.models import ChatUser, Ban


@api_view(["GET"])
def get_all_users(request):
    if request.session.get("login") != None and request.session.get("admin") == True:
        all_users = ChatUser.objects.filter(role_id__role_name = "user")
        json_users = {"users":[]}
        for user in all_users:
            b = Ban.objects.filter(user_id = user).first()
            json_user = {}
            json_user["name"] = user.name
            if b != None:
                json_user["rel"] = "remove"
                json_user["href"] = "http://"+request.get_host() + "/remove" + "/" + str(user.id)
            else:
                json_user["rel"] = "add"
                json_user["href"] = "http://" + request.get_host() + "/add"
            json_users["users"].append(json_user)

        return HttpResponse(json.dumps(json_users), content_type="applicaton/json", status=status.HTTP_200_OK)
    else:
        return HttpResponse("error login", status=400)

@csrf_exempt
@api_view(["POST"])
def add_user_to_black_list(request):
    if request.session.get("login") != None and request.session.get("admin") == True:
        json_data = JSONParser().parse(request)
        user_name = json_data["user"]
        print ("user name " + user_name)
        u = ChatUser.objects.filter(login = user_name).first()
        b = Ban(user_id=u)
        b.save()
        return HttpResponse("OK", status=200)
    else:
        return HttpResponse("login error", status=404)

@api_view(["DELETE"])
def remove_user_from_black_list(request, id):
    if request.session.get("login") != None and request.session.get("admin") == True:
        b = Ban.objects.filter(user_id__id = int(id))
        b.delete()
        return HttpResponse("OK", status=200)
    else:
        return HttpResponse("login error", status=404)


