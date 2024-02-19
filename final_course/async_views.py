import json
import random
import re

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from final_course import models, serializers


@sync_to_async
def get_history_messages_for_group(group_name):
    # Получение истории сообщений для группы
    messages = models.Message.objects.filter(group__slug=group_name)
    return [
        {
            "username": message.user.username,
            "message": message.content,
            "date_created": message.date_created,
        }
        for message in messages
    ]


@sync_to_async
def save_message_to_history(group_name, text_data):
    # Сохранение нового сообщения в истории
    data = json.loads(text_data)
    # print(data)
    # print(group_name)
    user = User.objects.get(username=data["user"]["username"])
    room = models.Group.objects.get(slug=group_name)
    models.Message.objects.create(user=user, group=room, content=str(data["message"]))


class GroupChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def save_message(self, username, room, message):
        # print(username, room, message)
        user = User.objects.get(username=username)
        room = models.Group.objects.get(slug=room)

        models.Message.objects.create(user=user, group=room, content=str(message))

    async def connect(self):
        # print(self.scope)
        self.room_name = self.scope["url_route"]["kwargs"]["group_name"]

        self.room_group_name = f"chat_online_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await get_history_messages_for_group(self.room_name)
        # print(messages)
        for message in messages:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "chat.message",
                        "message": message["message"],
                        "username": message["username"],
                        "timestamp": message["date_created"].isoformat(),
                    }
                )
            )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data: bytes):
        data = json.loads(text_data)  # bytes(JSON) -> dict
        # print("DATA:", data)

        username = data["user"]["username"]
        room = data["grSlug"]
        message = data["message"]

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "room": room,
            },
        )
        await save_message_to_history(self.room_name, text_data)
        await self.send(text_data=text_data)

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "room": room,
                }
            )
        )


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def create_group(request: Request) -> Response:
    if request.method == "POST":
        regex = r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{4,}$"
        form = request.data
        # print(form)
        name = str(form.get("name"))
        if not re.match(regex, name):
            return Response(
                data={"message": "Неправильное имя!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        is_private = bool(form.get("is_private_checkbox"))
        slug = name + "_" + str(random.randint(1, 1000000))
        owner = User.objects.get(username=request.user.username)

        owned_groups = Group.objects.filter(user=request.user)
        user_groups = request.user.groups.all()

        common_groups = owned_groups.intersection(user_groups)
        text = ""
        for group_ in common_groups:
            text += group_.name + " "

        if name is None or name == "":
            return Response(
                data={"error": "Заполните поле!"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if is_private:
                models.Group.objects.create(
                    name=name,
                    slug=slug,
                    owner=owner,
                    is_private=is_private,
                    user_in_group=text,
                )
            else:
                models.Group.objects.create(
                    name=name,
                    slug=slug,
                    owner=owner,
                )
            return Response(data={"success": True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            data={"message": "METHOD NOT ALLOWED"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def groups(request: Request) -> Response:
    user_groups = request.user.groups.all()

    text = ""
    for group_ in user_groups:
        text += group_.name + " "

    gr_obj = models.Group.objects.all()
    if request.method == "GET":
        try:
            group_objects_private = gr_obj.filter(user_in_group=text)
            data_private = serializers.GroupSerializer(
                group_objects_private, many=True
            ).data
            data = serializers.GroupSerializer(
                gr_obj.filter(user_in_group=None), many=True
            ).data
            # print("private: ", data_private, "public: ", data)
            return Response(
                data={"private": data_private, "public": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            data={"status": "METHOD NOT ALLOWED"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@permission_classes([IsAuthenticated])
def group(request: Request) -> Response:
    try:
        gr_objects = models.Group.objects.get(slug=request.GET.get("slug"))
        messages = models.Message.objects.filter(room=gr_objects)[::-1]
        data = serializers.MessageSerializer(messages, many=True)
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            data={"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
