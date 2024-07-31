from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Category, Author, Post, PostCategory, Comment, User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

# в декоратор передаётся первым аргументом сигнал, на который будет
# реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def send_email_createPost(sender, instance, action, **kwargs):
    if action == 'post_add':
        news = Post.objects.get(id=instance.id)
        b = PostCategory.objects.filter(post=instance.id).values('category')
        i = b[0]
        category = i.get('category')
        users = Category.objects.get(pk=category).subscribers.all()
        for user in users:
            if user.email:
                send_mail(

                    subject=news.title_news[:124] + "...",
                    # имя клиента и дата записи будут в теме для удобства
                    message=f'Здравствуй, {user}. Новая статья в твоём любимом разделе!    '
                            f'Краткое содержание:{news.text_news}...  '  # сообщение с кратким описанием проблемы
                            f'Портобнo  http://127.0.0.1:8000/{news.id}',
                    from_email='izorgin.pasha@yandex.ru',
                    # здесь указываете почту, с которой будете отправлять (об этом попозже)
                    recipient_list=[user.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
                )
            else:
                print("not email")
        pass
