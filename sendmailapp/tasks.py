
from celery.decorators import task
from celery.utils.log import get_task_logger
# from .email import send_review_email
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
import time



from celery import shared_task


logger = get_task_logger(__name__)

@task(name="send_review_email_task")
def send_review_email_task(subject,message,htmls , to):

    logger.info("Sent email")
#    email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL ,to)
#    return email.send(fail_silently=False)

    email = EmailMultiAlternatives(subject,message,settings.DEFAULT_FROM_EMAIL,to,)
    email.attach_alternative(htmls,"text/html")
    email.send()








