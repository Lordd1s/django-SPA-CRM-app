from django.contrib.auth.models import User
from rest_framework import serializers
from final_course import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "groups",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.UserProfile
        fields = "__all__"


class VacanciesSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = models.Vacancy
        fields = "__all__"


class CVSerializer(serializers.ModelSerializer):
    job_title = VacanciesSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = models.CV
        fields = "__all__"


class CVSerializerDownload(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    job_title = serializers.CharField(source="job_title.title", read_only=True)

    class Meta:
        model = models.CV
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "where_from",
            "job_title",
            "created_at",
        ]


class LikeSerializer(serializers.ModelSerializer):
    date_clicked = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = models.Like
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    _user = UserSerializer(read_only=True)

    class Meta:
        model = models.Application
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = models.Group
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    _user = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = models.Message
        fields = "__all__"
