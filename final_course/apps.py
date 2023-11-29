from django.apps import AppConfig


class FinalCourseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "final_course"

    def ready(self):
        import final_course.signals
