from django.contrib.sessions.models import Session
from redis.sentinel import Sentinel
import sockjs.tornado
import json

from chatApp.models import ChatUser, Message


class SocketHandler(sockjs.tornado.SockJSConnection):
    active_clients = {} #dictionary with usernames and sockets
    session_active_clients = {} #dictionary with logins and sessions
    sentinel = Sentinel([("127.0.0.1", 17777)],socket_timeout=0.1)
    nosqldatabase = sentinel.master_for("mymaster", socket_timeout=0.1)
    def on_open(self, request):
        print("Socket is opened")

    def on_message(self, message):
        json_message = json.loads(message)
        if (json_message.get("sessionid")!=None):
            sessionid = json_message["sessionid"]
            session = Session.objects.get(session_key=sessionid)
            session_data = session.get_decoded()
            login = session_data.get('login')
            answer = {}
            if login == None:
                answer["auth"]="no"
            else:
                answer["auth"]="yes"
                SocketHandler.active_clients[login]=self
                SocketHandler.session_active_clients[login]=sessionid
                self.send_list_activeusers()
                self.send_user_all_messages()
            self.send(json.dumps(answer))
        client = self.get_client()
        if (client != None and json_message.get("broadcast")!=None):
            broadcast_message = json_message["broadcast"]
            SocketHandler.nosqldatabase.lpush("broadcast",client+":"+broadcast_message)
            answer = {}
            answer["auth"]="yes"
            answer["name"]=client
            answer["message"]=broadcast_message

            for socket in SocketHandler.active_clients.values():
                socket.send(json.dumps(answer))
        if (client !=None and json_message.get("name")!=None):
            receiver = json_message.get("name")
            sender = client
            message = json_message.get("message")
            receiver_socket = SocketHandler.active_clients.get(receiver)
            if receiver_socket == None:
                resv = ChatUser.objects.filter(login=receiver).first()
                sendr = ChatUser.objects.filter(login=sender).first()
                m = Message(body=message, sender_id=sendr, receiver_id = resv)
                m.save() #save to postgresql DB
            else:
                answer = {}
                answer["auth"] = "yes"
                answer["name"]=sender
                answer["message"]=message
                receiver_socket.send(json.dumps(answer))
        if (client !=None and json_message.get("logout")!=None):
            logout_socket=SocketHandler.active_clients[client]
            del SocketHandler.active_clients[client]
            sessionid=SocketHandler.session_active_clients[client]
            Session.objects.filter(session_key=sessionid).delete()
            del SocketHandler.session_active_clients[client]
            self.send_list_activeusers()
            answer={}
            answer["auth"] = "yes"
            answer["logout"] = ""
            logout_socket.send(json.dumps(answer))

    def on_close(self):
        print("Socket is closed")


    def send_list_activeusers(self):
        #print("list")
        answer={}
        answer["auth"] = "yes"
        answer["list"] = []
        for user in SocketHandler.active_clients.keys():
            answer["list"].append(user)
        #print(answer["list"])
        for socket in SocketHandler.active_clients.values():
            socket.send(json.dumps(answer))

    def send_user_all_messages(self):
        client = self.get_client()
        messages = Message.objects.filter(receiver_id__login=client)
        #from postrgresql
        for message in messages:
            answer = {}
            answer["auth"] = "yes"
            chat_user = ChatUser.objects.filter(id=message.sender_id_id).first()
            answer["name"] = chat_user.login
            answer["message"] = message.body
            self.send(json.dumps(answer))
            Message.objects.filter(receiver_id__login=client).delete()
        for broadcast_message in SocketHandler.nosqldatabase.lrange("broadcast",0,-1):
            broadcast_message_array = str(broadcast_message).split(":")
            answer = {}
            answer["auth"] = "yes"
            answer["name"] = broadcast_message_array[0]
            answer["message"] = broadcast_message_array[1]
            self.send(json.dumps(answer))

    def get_client(self):
        for key,value in SocketHandler.active_clients.items():
            if value == self:
                return key




