import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ...models import *

logger = logging.getLogger(__name__)

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

class Command(BaseCommand):
    help = 'Runs apscheduler'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone = settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            mail_distributon,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id='mail_distribution',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job mail_distribution')
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")