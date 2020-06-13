# from django.forms import ModelForm
# from hitchify.models import Comment

from django import forms
from django.forms import SelectDateWidget

from . import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body_text', 'parent_comment']


class AddPostForm(forms.ModelForm):
    class Meta:
        model = models.ForumPost
        fields = ['title', 'body_text']


class AddGuideForm(forms.ModelForm):
    class Meta:
        model = models.Guide
        fields = ['title', 'body_text', 'short_summary']


class AddCountryForm(forms.ModelForm):
    class Meta:
        model = models.Country
        fields = ['country_name', 'short_description', 'national_currency']


class CustomSignUpForm(UserCreationForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    res_country = forms.CharField()
    res_city = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'birth_date', 'gender', 'res_country', 'res_city']
        # widgets = {
        #     'birth_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }
