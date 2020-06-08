# from django.forms import ModelForm
# from hitchify.models import Comment

from django import forms
from . import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body_text']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = models.ForumPost
        fields = ['title', 'body_text']
