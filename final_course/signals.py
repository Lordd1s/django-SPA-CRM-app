import asyncio

import telegram_notification

from django.core.cache import cache
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from final_course import models
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        models.UserProfile.objects.create(user=instance, was_born=None)


@receiver(post_save, sender=models.CV)
def rating(sender, instance, created, **kwargs):
    if created:
        """
        Создает рейтинг на основе заполненных полей!
        """
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
            if getattr(instance, field_name, None) != "":
                filled_fields += 1
            total_fields += 1

        if filled_fields > 0:
            new_rating = (filled_fields / total_fields) * 100
            # print("Rating", new_rating)
        else:
            new_rating = 0.0

        if new_rating != instance.rating:
            instance.rating = new_rating
            instance.save()


@receiver(post_save, sender=models.CV)
def cache_autorefresh_cv(sender, instance, **kwargs):
    if instance:
        cache_key = "all_cv"
        cache_key_boss = "all_cv_boss"
        cache.delete(cache_key)
        cache.delete(cache_key_boss)
        print("Кэш удален CV")


@receiver(post_save, sender=models.Vacancy)
def cache_autorefresh_vacancy(sender, instance, **kwargs):
    if instance:
        cache_key = "vacancy"
        cache.delete(cache_key)
        print("Кэш удален Vacancy")


@receiver(post_save, sender=models.Application)
def cache_autorefresh_application_masters(sender, instance, **kwargs):
    if instance:
        cache.delete("application")
        cache.delete("applications")
        type_of = ""
        is_accepted = ""
        match instance.type_of:
            case "X":
                type_of += "Хлыст"
            case "B":
                type_of += "Бухта"
        print("Кэш удален 'Заявка'")
        match instance.is_accepted:
            case "0":
                is_accepted += "ОТКЛОНЕНО!"
            case "1":
                is_accepted += "ПРИНЯТО!"
            case "2":
                is_accepted += "НЕ РЕШЕНО!"
        message_text = f"""
            <b>Заявка от:</b> {instance._user.username}
            
<b>Статус:</b> {is_accepted}

<b>Диаметр трубы:</b> {instance.diameter}

<b>Толщина трубы:</b> {instance.thickness}

<b>Длина труб:</b> {instance.length}

<b>Объекту:</b> {instance.object_to}

<b>Тип перевозки:</b> {type_of}


<b>Дата заявки:</b> {instance.date_created}
            
        """

        asyncio.run(telegram_notification.get_application(application=message_text))
