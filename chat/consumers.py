from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Salon, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def fetch_messages(self, data):
        salon = data['classe']
        messages = await sync_to_async(
            lambda: list(Message.objects.filter(salon__classe=int(salon)).order_by('date_add')[:20])
        )()
        content = {
            'command': 'messages',
            'messages': await self.messages_to_json(messages)
        }
        await self.send_message(content)

    async def new_message(self, data):
        auteur = data['from']
        salon = data['classe']
        salon_object = await sync_to_async(Salon.objects.get)(classe__id=int(salon))
        auteur_user = await sync_to_async(User.objects.get)(username=auteur)
        message = await sync_to_async(Message.objects.create)(
            auteur=auteur_user,
            salon=salon_object,
            message=data['message']
        )
        content = {
            'command': 'new_message',
            'message': await self.message_to_json(message)
        }
        await self.send_chat_message(content)

    async def messages_to_json(self, messages):
        return [await self.message_to_json(message) for message in messages]

    async def message_to_json(self, message):
        try:
            image = await sync_to_async(lambda: message.auteur.student_user.photo.url)()
        except AttributeError:
            image = await sync_to_async(lambda: message.auteur.instructor.photo.url)()
        return {
            'auteur': await sync_to_async(lambda: message.auteur.username)(),
            'auteur_image': image,
            'message': await sync_to_async(lambda: message.message)(),
            'date_add': await sync_to_async(lambda: message.date_add.strftime("%Y-%m-%d %H:%M:%S"))()
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    async def connect(self):
        self.salon = self.scope['url_route']['kwargs']['classe']
        self.room_group_name = f'chat_{self.salon}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
