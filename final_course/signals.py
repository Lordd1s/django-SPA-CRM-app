from django.core.cache import cache
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from final_course import models


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
            print("Rating", new_rating)
        else:
            new_rating = 0.0

        if new_rating != instance.rating:
            instance.rating = new_rating
            instance.save()


# @receiver(post_save, sender=models.CV)
# def rating_plus_cahce(sender, instance, update_fields=None, **kwargs):
#     if instance:
#         cache_key = "all_cv"
#         cache.delete(cache_key)
#         print("Кэш обновлен CV")
#
#
# @receiver(post_save, sender=models.Vacancy)
# def cache_autorefresh(sender, instance, **kwargs):
#     if instance:
#         cache_key = "vacancy"
#         cache.delete(cache_key)
#         print("Кэш обновлен Vacancy")
