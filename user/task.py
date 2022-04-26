from celery import shared_task
from django.core.mail import send_mail
# from fundooNotes import settings
from django.conf import settings


@shared_task(bind=True)
def send_email(self, to_email, token):
    send_mail(from_email=settings.EMAIL_HOST, recipient_list=[to_email],
              message="Thanks for using fundooNotes services\n Your activation token = "
                      "http://127.0.0.1:8000/user/api/{}".format(token),
              subject="Registration link", fail_silently=False, )
    return "Registration Done"
