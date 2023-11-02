from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    group_name = ""

    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"notification_group_{self.user.username}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send(text_data="HOLA, Established Connection Over Websocket. 🎉")

    async def disconnect(self, close_code):
        await self.close()
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
