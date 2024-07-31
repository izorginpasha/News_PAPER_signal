from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Post, Category, PostCategory


class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ['author', 'products', 'title_news', 'text_news', 'post_reiting']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user