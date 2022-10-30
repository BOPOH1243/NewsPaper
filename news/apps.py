from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    def ready(self):
        import news.signals

        from .tasks import mail_distributon
        from .scheduler import mail_scheduler
        print('started')

        """mail_scheduler.add_job(
            id='mail distribution',
            func=mail_distributon,
            trigger='interval',
            seconds=20,
            #trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
        )
        mail_scheduler.start()"""
