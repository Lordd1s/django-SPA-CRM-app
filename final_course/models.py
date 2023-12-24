from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        verbose_name="Аватар пользователя",
        upload_to="avatars/",
        blank=True,
        default="avatars/6596121.png",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "gif", "jpeg"]),
        ],
    )
    was_born = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Номер телефона"
    )

    class Meta:
        app_label = "final_course"
        ordering = ["-was_born"]
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return self.user.username


class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название", unique=True)
    description = models.TextField(verbose_name="Описание")
    date_created = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    required_person = models.SmallIntegerField(
        default=0, verbose_name="Требуемый персонал"
    )

    class Meta:
        app_label = "final_course"
        ordering = ["-date_created", "is_active"]
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title


class CV(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(
        max_length=100, verbose_name="Отчество", null=True, blank=True
    )
    was_born = models.DateField(
        verbose_name="Дата рождения",
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
    )
    photo = models.ImageField(
        upload_to="photos/", blank=True, null=True, verbose_name="Фото"
    )
    where_from = models.CharField(max_length=100, verbose_name="Место рождения")
    where_to = models.CharField(
        max_length=100, verbose_name="Место жительства", null=True, blank=True
    )
    education = models.CharField(
        max_length=100, verbose_name="Образование", null=True, blank=True
    )
    job_xp = models.CharField(
        max_length=100, verbose_name="Опыт работы", null=True, blank=True
    )
    job_title = models.ForeignKey(
        to=Vacancy,
        max_length=100,
        verbose_name="Должность",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    skills = models.CharField(
        max_length=100, verbose_name="Навыки", null=True, blank=True
    )
    languages = models.CharField(
        max_length=100, verbose_name="Языки", null=True, blank=True
    )
    about_me = models.TextField(verbose_name="О себе", null=True, blank=True)
    is_viewed = models.BooleanField(default=False, verbose_name="Просмотрено")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата отправки"
    )
    is_accept = models.BooleanField(default=False, verbose_name="Подтверждено")
    is_declined = models.BooleanField(default=False, verbose_name="Отклонен")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")

    class Meta:
        app_label = "final_course"
        ordering = ["-was_born", "first_name", "last_name"]
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return f"Резюме от {self.first_name} {self.last_name}"


class Like(models.Model):
    which_cv = models.ForeignKey(
        to=CV, verbose_name="Какому резюме?", on_delete=models.CASCADE
    )
    clicked_by = models.ForeignKey(
        to=User, verbose_name="Кто поставил?", on_delete=models.CASCADE
    )
    status = models.BooleanField(default=False)
    date_clicked = models.DateTimeField(
        default=timezone.now, verbose_name="Когда поставлено?"
    )

    class Meta:
        app_label = "final_course"
        ordering = ["-date_clicked", "clicked_by"]
        verbose_name = "Одобрение"
        verbose_name_plural = "Одобрении"

    def __str__(self):
        if self.status:
            return f"{self.clicked_by} {self.which_cv} одобряет"
        else:
            return f"{self.clicked_by} {self.which_cv} не одобряет"


class Application(models.Model):
    _user = models.ForeignKey(
        to=User, verbose_name="Подал заявку", on_delete=models.DO_NOTHING
    )
    diameter = models.SmallIntegerField(
        verbose_name="Диаметр труб",
    )
    thickness = models.SmallIntegerField(verbose_name="Толщина труб")
    length = models.IntegerField(verbose_name="Длина труб")
    LIST_OF_TYPE_CHOICES = [("X", "Хлыст"), ("B", "Бухта")]
    type_of = models.CharField(max_length=1, choices=LIST_OF_TYPE_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)
    object_to = models.CharField(
        max_length=30, verbose_name="Объект", null=True, blank=True
    )
    LIST_OF_ACCEPTED_CHOICES = [
        ("0", "Отклонено"),
        ("1", "Принято"),
        ("2", "Не решено"),
    ]
    is_accepted = models.CharField(
        max_length=1,
        default=LIST_OF_ACCEPTED_CHOICES[-1][0],
        choices=LIST_OF_ACCEPTED_CHOICES,
    )

    class Meta:
        app_label = "final_course"
        ordering = ("-date_created", "diameter", "thickness", "length")
        verbose_name = "Заявка на трубу"
        verbose_name_plural = "Заявки на трубы"

    def __str__(self):
        return f"Заявка от {self._user}, по дате {self.date_created}"


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя группы")
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.DO_NOTHING, null=True
    )
    is_private = models.BooleanField(default=False, verbose_name="Видимость")
    user_in_group = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = "final_course"
        ordering = ("name", "owner")
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Message(models.Model):
    group = models.ForeignKey(Group, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Контент (текст сообщений)")
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-date_created",)
