from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import *

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