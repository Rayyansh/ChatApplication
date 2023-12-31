import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)

    def receive(self,text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['username']
        print(user)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{"type": "chat.message","message": message, 'user': user})

        # self.send(text_data=json.dumps({'message':message}))

    def chat_message(self,event):
        message = event['message']
        user = event['user']
        self.send(text_data=json.dumps({'message': message,'user': user}))
