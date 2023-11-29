import json
import logging

from django.core.cache import cache
from django.views.decorators.cache import cache_page

from final_course import utils


from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.core.validators import EmailValidator

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from final_course import serializers, models, permission


logger = logging.getLogger(__name__)

MESSAGE = {
    "message_created": "Успешно создана!",
    "message_updated": "Успешно обновлен!",
    "message_deleted": "Успешно удален!",
    "message_error": "Ошибка",
}


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    """
    Этот контроллер отвечает за вход на главную страницу!

    :param request: HttpRequest: Get the request object
    :return: A HttpResponse object
    :doc-author: Dias
    """

    return render(request=request, template_name="home.html")


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def register(request: Request) -> Response:
    """
    Функция register используется для регистрации нового пользователя.

    :param request: Request: Get the request data
    :return: A response object
    :doc-author: Dias
    """
    if request.method == "POST":
        form = json.loads(request.body)
        username = form.get("username")
        password = form.get("password")
        email = form.get("email")

        if not (username and password and email):
            return Response(
                data={"error": "Не все поля заполнены."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                data={"error": "Пользователь с таким email уже существует."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if EmailValidator(email):
                User.objects.create(
                    username=username,
                    password=make_password(password),
                    email=email,
                )
                return Response(
                    data=MESSAGE["message_created"],
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                data={"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def login_user(request: Request, pk) -> Response:
    try:
        if request.method == "GET":
            user = get_object_or_404(User, pk=pk)
            data = serializers.UserSerializer(user).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"message": "Method not allowed"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
    except Http404:
        return Response(
            data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(http_method_names=["POST", "PUT", "DELETE"])
@permission_classes([AllowAny])
def cv(request: Request, pk=None) -> Response:
    """

    :param pk:
    :param request:
    :return:
    """
    if request.method == "POST":
        # print(request.data)
        # print(request.data.get("photo"))
        # print(request.FILES.get("photo"))
        form = request.data
        first_name = form.get("name")
        last_name = form.get("lastName")
        middle_name = form.get("middleName")
        was_born = form.get("wasBorn")
        phone_number = form.get("phone_number")
        photo = form.get("photo")
        where_from = form.get("whereFrom")
        where_to = form.get("whereTo")
        job_title = models.Vacancy.objects.get(title=form.get("jobTitle"))
        job_xp = form.get("jobXp")
        education = form.get("education")
        skills = form.get("skills")
        languages = form.get("languages")
        about_me = form.get("aboutMe")

        if models.CV.objects.filter(
            last_name=last_name, first_name=first_name, middle_name=middle_name
        ).exists():
            return Response(
                data={"error": "Резюме с такими данными уже существует."},
                status=status.HTTP_403_FORBIDDEN,
            )

        models.CV.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            was_born=was_born,
            phone_number=phone_number,
            photo=photo,
            where_from=where_from,
            where_to=where_to,
            job_title=job_title,
            job_xp=job_xp,
            education=education,
            skills=skills,
            languages=languages,
            about_me=about_me,
        )

        return Response(
            data=MESSAGE["message_created"],
            status=status.HTTP_201_CREATED,
        )
    elif request.method == "PUT":
        if pk:
            get_cv = get_object_or_404(models.CV, id=int(pk))
            get_cv.is_viewed = True
            if request.data.get("is_accept"):
                get_cv.is_accept = True
            if request.data.get("is_declined"):
                get_cv.is_declined = True
            try:
                get_cv.save()
                return Response(
                    data=MESSAGE["message_updated"], status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    data={"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data={"Аргумент не поддерживается!"}, status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == "DELETE":
        try:
            get_object_or_404(models.CV, id=int(pk)).delete()
            return Response(data=MESSAGE["message_deleted"], status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
# @cache_page(60 * 60)
def vacancy(request: Request) -> Response:
    """
    Для показа всех вакансий пользователю! (Не требует входа)

    :param request: Request: Get the request data from the client
    :return: A list of active vacations
    :doc-author: Dias
    """
    if request.method == "GET":
        print(request.user)
        try:
            if request.user.is_superuser or request.user.is_staff:
                vacations = models.Vacancy.objects.all()
                print("SU or Staff")
            else:
                vacations = models.Vacancy.objects.filter(is_active=True)
                print("anonym")
            serializer = serializers.VacanciesSerializer(vacations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                data={"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated, permission.IsInGroupPermission])
# @cache_page(60 * 60)
def all_cv(request: Request) -> Response:
    """
    Показывает все резюме только у кого есть права!

    :param request: Request: Get the request data from the client
    :return: A list of CV
    :doc-author: Dias
    """
    try:
        serializer = serializers.CVSerializer(models.CV.objects.all(), many=True)
        # print(serializer.data[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            data={"message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(http_method_names=["POST", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_vacancy(request: Request, pk=None) -> Response:
    """
    Создание, обновление, удаление вакансии! Доступно только SU & admins

    :param request: Request: Принимает запрос от клиента
    :param pk: str: Принимает id объекта в БД
    :return: При успешной отправки возвращает 200 или 201
    :doc-author: Dias
    """
    form = request.data
    print(form)
    title = form.get("title")
    description = form.get("description")
    is_active = form.get("is_active")
    required_person = form.get("required_person")

    if request.method == "POST":
        if not title or not description or not required_person:
            return Response(
                data={"message": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            models.Vacancy.objects.create(
                title=title, description=description, required_person=required_person
            )
            return Response(
                data=MESSAGE["message_created"], status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    if pk:
        get_vacancy = models.Vacancy.objects.get(id=int(pk))
        if request.method == "PUT" or request.method == "PATCH":
            if not title or not description or not required_person:
                return Response(
                    data={"message": "All fields are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            get_vacancy.title = title
            get_vacancy.description = description
            get_vacancy.is_active = is_active
            get_vacancy.required_person = required_person

            try:
                get_vacancy.save()
                return Response(
                    data=MESSAGE["message_updated"], status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        elif request.method == "DELETE":
            try:
                get_vacancy.delete()
                return Response(
                    data=MESSAGE["message_deleted"], status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
