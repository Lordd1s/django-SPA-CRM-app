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

    def save(self, *args, **kwargs):
        total_fields = 0
        filled_fields = 0

        fields_to_check = [
            "middle_name",
            "photo",
            "where_to",
            "education",
            "job_xp",
            "skills",
            "languages",
            "about_me",
        ]

        for field_name in fields_to_check:
            if getattr(self, field_name, None) is not None:
                filled_fields += 1
            total_fields += 1

        if total_fields > 0:
            new_rating = (filled_fields / total_fields) * 100
        else:
            new_rating = 0.0

        if new_rating != self.rating:
            self.rating = new_rating
            super(CV, self).save(*args, **kwargs)
        else:
            super(CV, self).save(*args, **kwargs)

    def __str__(self):
        return f"Резюме от {self.first_name} {self.last_name}"
