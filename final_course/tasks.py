from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone

from final_course.models import CV


@shared_task
def summary(x, y):
    return x + y


@shared_task
def send_cv():
    filtered_cv = CV.objects.filter(created_at__date=timezone.now().date())
    if filtered_cv.exists():
        users = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True))
        users_email = [u.email for u in users]
        message = ""
        for cv in filtered_cv:
            message_text = f"""
                Поступило резюме от {cv.first_name}
    
    
                Имя кандидата: {cv.first_name}
                Фамилия кандидата: {cv.last_name}
                Позиция, на которую претендует: {cv.job_title.title}
                Номер телефона: {cv.phone_number}
                
                \n
            """
            message += message_text

        message += """
            
            \n Благодарим за ваше внимание!
    
            С наилучшими пожеланиями, 
                
            Диас
            """

        print(message)

        if len(users_email) <= 0:
            raise ValueError(f"Почты нету! {users_email}")
        else:
            try:
                send_mail(
                    "Новое Резюме!",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=users_email,
                    auth_user=settings.EMAIL_HOST_USER,
                    auth_password=settings.EMAIL_HOST_PASSWORD,
                    fail_silently=False,
                )
                print("Success")
            except Exception as e:
                raise e
    else:
        print("Нет резюме за сегодня!")
        return None
