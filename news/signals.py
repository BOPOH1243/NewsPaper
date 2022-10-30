from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from .tasks import send_subscribers_email
# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=User)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        user = instance
        html_content = render_to_string(
            'mail/greeting.html',
            {
                'user': user,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'приветствую тебя, юзер {user.username}',
            body=user.username,  # это то же, что и message
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


@receiver(post_save,sender=Post)
def send_post_for_subscribers_on_email(sender,instance,created, **kwargs):
    if created:
        post = instance
        send_subscribers_email.delay(post.pk)
