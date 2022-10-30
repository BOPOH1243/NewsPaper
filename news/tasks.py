from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import *
from celery import shared_task
import time
from celery.schedules import crontab
from NewsPaper.celery import app


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def mail_distributon():
    print('mail_distribution')
    for user in User.objects.all():
        posts = []
        for subscribes in UserSubscribe.objects.filter(user=user):
            for post in Post.objects.filter(categories__pk=subscribes.category.pk):
                if not post in posts and len(posts)<8:
                    posts.append(post)

        html_content = render_to_string(
            'mail/schedule_news.html',
            {
                'news': posts,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'последние новости',
            body=user.username,  # это то же, что и message
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        try:
            msg.send()
        except:
            pass


@shared_task
def send_subscribers_email(post_pk):
    post = Post.objects.get(pk=post_pk)
    subscribers = post.post_subscribers()
    html_content = render_to_string(
        'mail/subscribe_news.html',
        {
            'new': post,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Новость по подписке {post.header}',
        body=post.preview(length=50),  # это то же, что и message
        from_email=settings.EMAIL_HOST_USER,
        to=[i.email for i in subscribers],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'mail_distribution',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (None),
    },
}