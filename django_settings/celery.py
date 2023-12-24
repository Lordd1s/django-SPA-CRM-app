import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")
app = Celery("django_settings")
app.config_from_object("django.conf:settings", namespace="CELERY")  # CELERY_Name

app.conf.beat_schedule = {
    "send_cv": {
        "task": "final_course/tasks.send_cv",
        "schedule": crontab(minute="0", hour="0"),
    }
}

app.autodiscover_tasks()
