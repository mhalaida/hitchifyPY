import os

from django.contrib.auth import login as my_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from hitchify.models import Comment, Country, ForumPost, Guide, \
    GuideFeedback, Hitchspot, Language, \
    LanguageToCountry, Photo, SpotFeedback, \
    UserLikedComment, UserLikedForumPost

from . import forms
from django.db import connection

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def like_post(request, post_id):

    post = ForumPost.objects.get(id = post_id)
    user = request.user

    # if request.method == 'POST':

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user_liked_forum_post (user_id, post_id) "
            "VALUES (%s, %s)",
            [user.id, post.id])

    with connection.cursor() as cursor:
        cursor.execute('UPDATE forum_post '
                       'SET likes = likes + 1 '
                       'WHERE id = %s', [post_id])

    return redirect('post', post_id)


def add_post(request, country_id):

    country = Country.objects.get(id=country_id)

    if request.method == 'POST':
        form = forms.AddPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.country = country
            new_post.user = request.user
            new_post.save()
            return redirect('country', country_id)

        else:
            form = forms.AddPostForm()

        return render(request, 'country.html', {'form': form, 'country': country})


def add_comment_to_post(request, post_id):
    post = ForumPost.objects.get(post_id=post_id)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_comment_to_post')

        else:
            form = forms.CommentForm()
        return render(request, 'post.html', {'form': form, 'post': post})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            # my_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, os.path.join(BASE_DIR, 'templates/registration/signup.html'), {'form': form})


def add_point(request):
    if request.method == 'POST':
        from django.db import connection

        description = request.POST['description']
        avg_hitchability = request.POST['avg_hitchability']
        avg_waiting_time = request.POST['avg_waiting_time']
        ln = request.POST['ln']
        lt = request.POST['lt']
        country_id = request.POST['country_id']
        user_id = request.POST['user_id']

        if description == '':
            description = '-'

        if avg_hitchability == '':
            avg_hitchability = '1'

        if avg_waiting_time == '':
            avg_waiting_time = '1'

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO hitchspot (id, latitude, longitude, description, avg_hitchability, avg_waiting_time, creation_date, last_update, country_id,user_id)"
            " VALUES (nextval('spot_sequence'), %s, %s, %s, %s, %s, now(), now(), %s, %s)",
            [lt, ln, description, avg_hitchability, avg_waiting_time, country_id, user_id])

    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) AS spot_count '
                       'FROM hitchspot '
                       'GROUP BY country_id '
                       'HAVING country_id = %s', [country_id])
        spots_num = cursor.fetchone()

    with connection.cursor() as cursor:
        cursor.execute('SELECT SUM(avg_hitchability) AS spot_hitchability_sum '
                       'FROM hitchspot '
                       'GROUP BY country_id '
                       'HAVING country_id = %s', [country_id])
        spots_hitchability_sum = cursor.fetchone()

    res = round((spots_hitchability_sum[0] / spots_num[0]), 2)

    with connection.cursor() as cursor:
        cursor.execute('UPDATE country '
                       'SET hitchrating = %s '
                       'WHERE id = %s', [res, country_id])

    country = Country.objects.get(id=country_id)

    context = {
        'country': country,
        'choose': 'map',
    }

    return render(request, 'map_country.html', context=context)


def login(request):
    context = {}

    return render(request, os.path.join(BASE_DIR, 'templates/registration/login.html'), context=context)


def countries(request):
    countries = Country.objects.all()

    context = {
        'choose': 'country',
        'countries': countries
    }

    return render(request, 'countries.html', context=context)


def country(request, country_id):
    country = Country.objects.get(id=country_id)

    context = {
        'choose': 'country',
        'country': country
    }

    return render(request, 'country.html', context=context)


def hitchspots(request):
    hitchspot = Hitchspot.objects.all()

    context = {
        'hitchspot': hitchspot
    }

    return render(request, 'hitchspots.html', context=context)


def forum(request):
    forum = ForumPost.objects.all()

    context = {
        'forum': forum
    }

    return render(request, 'forum.html', context=context)


def post(request, post_id):
    post = ForumPost.objects.get(id=post_id)

    context = {
        'post': post
    }

    return render(request, 'post.html', context=context)


def guides(request):
    guides = Guide.objects.all()

    context = {
        'guides': guides
    }

    return render(request, 'guides.html', context=context)


def guide(request):
    context = {}

    return render(request, 'guide.html', context=context)


def hitchify_map(request):
    context = {
        'choose': 'map',
    }

    return render(request, 'map.html', context=context)


def hitchify_map_country(request, country_id):
    country = Country.objects.get(id=country_id)

    context = {
        'country': country,
        'choose': 'map',
    }

    return render(request, 'map_country.html', context=context)


def hitchify_xml(request):
    hitchspots = Hitchspot.objects.all()

    context = {'hitchspots': hitchspots}

    return render(request, 'map_xml.html', context=context, content_type="application/xhtml+xml")


def hitchify_xml_country(request, country_id):
    hitchspots = Hitchspot.objects.raw('SELECT * '
                                       'FROM hitchspot '
                                       'WHERE country_id = %s', [country_id])

    context = {'hitchspots': hitchspots}

    return render(request, 'map_xml.html', context=context, content_type="application/xhtml+xml")
