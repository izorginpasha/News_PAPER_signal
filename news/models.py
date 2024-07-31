from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_reiting = models.IntegerField(default=0)

    def update_reting(self):
        sum_reiting_post = 0
        sum_reiting_comment = 0
        sum_reiting_commentNews = 0
        post = Post.objects.filter(author=self)
        for p in post:
            sum_reiting_post += p.post_reiting
        comment = Comment.objects.filter(user=self.user)
        for c in comment:
            sum_reiting_comment += c.comment_reiting
        p_comment = Comment.objects.filter(post__author=self)
        for pc in p_comment:
            sum_reiting_commentNews += pc.comment_reiting

        self.user_reiting = (sum_reiting_post * 3) + (sum_reiting_comment) + (sum_reiting_commentNews)
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=55, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')


class Post(models.Model):
    article = 'статья'
    news = 'новость'

    POSITIONS = [
        (article, 'article'),
        (news, 'news'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = models.CharField(max_length=55, choices=POSITIONS, default='новость')
    time_in = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Category, through='PostCategory', related_name='followers',symmetrical=False)
    title_news = models.CharField(max_length=55)
    text_news = models.TextField(default="Текст отсутствует")
    post_reiting = models.IntegerField(default=0)



    def like(self):
        self.post_reiting = self.post_reiting + 1
        self.save()

    def dislike(self):
        self.post_reiting -= 1
        self.save()

    def preview(self):
        return self.text_news[:124] + "..."

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(default="Текст отсутствует")
    time_in = models.DateTimeField(auto_now_add=True)
    comment_reiting = models.IntegerField(default=0)

    def like(self):
        self.comment_reiting = self.comment_reiting + 1
        self.save()

    def dislike(self):
        self.comment_reiting -= 1
        self.save()
