from django.contrib.auth.models import User
from rest_framework import serializers
from final_course import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
