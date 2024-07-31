import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

import time
from datetime import datetime
from datetime import timedelta
from news.models import Category, Author, Post, PostCategory, Comment, User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...
    print('hello from job')
    now = datetime.now()
    new_date = now - timedelta(days=7)
    post_list = Post.objects.filter(time_in__range=(new_date, now)).all()
    users = User.objects.all()
    for user in users:
        if user.email:
            for post in post_list:
                send_mail(
                    subject='send',
                    # имя клиента и дата записи будут в теме для удобства
                    message=f'Здравствуй, {user}. Новая статьи!    '
                            f'Краткое содержание:{post.text_news[:124] + "..."}'  # сообщение с кратким описанием проблемы
                            f'Портобнo  http://127.0.0.1:8000/{post.id}',
                    from_email='izorgin.pasha@yandex.ru',
                    # здесь указываете почту, с которой будете отправлять (об этом попозже)
                    recipient_list=[user.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
                )


        else:
            print("not email")


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='6', hour='8'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")