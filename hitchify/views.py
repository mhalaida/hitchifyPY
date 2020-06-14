import os

from django.contrib.auth import login as my_login, authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from hitchify.models import Comment, Country, ForumPost, Guide, \
    GuideFeedback, Hitchspot, Language, \
    LanguageToCountry, Photo, SpotFeedback, \
    UserLikedComment, UserLikedForumPost

from . import forms
from django.db import connection

from .forms import CustomSignUpForm

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

            user = request.user
            body_text = request.POST['body_text']
            title = request.POST['title']

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO forum_post (id, body_text, creation_date, title, country_id, user_id) "
                    "VALUES (nextval('forum_post_id_seq'), %s, now(), %s, %s, %s)",
                    [body_text, title, country_id, user.id])

            return redirect('country_post', country_id)

    else:
        form = forms.AddPostForm()

    return render(request, 'new_post.html', {'form': form, 'country': country})


def edit_post(request, post_id):

    if request.method == 'POST':
        form = forms.AddPostForm(request.POST)
        if form.is_valid():
            user = request.user

            posts = ForumPost.objects.raw("SELECT * "
                                          "FROM forum_post "
                                          "WHERE id = %s AND user_id = %s",
                                          [post_id, user.id])

            title = request.POST['title']
            body_text = request.POST['body_text']

            # перевіряємо дозволи - адмін/модератор або власник коментаря
            if user.has_perm("hitchify.change_forumpost") or user.id == posts[0].user_id:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE forum_post SET body_text = %s, title = %s, last_update = now() WHERE id = %s",
                        [body_text, title, post_id])

    return redirect('post', post_id)


@permission_required('hitchify.change_guide')
def edit_guide(request, guide_id):

    if request.method == 'POST':
        form = forms.AddGuideForm(request.POST)
        if form.is_valid():

            title = request.POST['title']
            body_text = request.POST['body_text']
            short_summary = request.POST['short_summary']

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE guide SET body_text = %s, short_summary = %s, title = %s, update_date = now() WHERE id = %s",
                    [body_text, short_summary, title, guide_id])

    return redirect('guide', guide_id)


@permission_required('hitchify.change_country')
def edit_country(request, country_id):

    if request.method == 'POST':
        form = forms.AddCountryForm(request.POST)
        if form.is_valid():

            country_name = request.POST['country_name']
            short_description = request.POST['short_description']
            national_currency = request.POST['national_currency']

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE country SET country_name = %s, short_description = %s, national_currency = %s "
                    "WHERE id = %s",
                    [country_name, short_description, national_currency, country_id])

    return redirect('country', country_id)


def add_comment_to_post(request, post_id):

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():

            user = request.user
            body_text = request.POST['body_text']
            parent_comment_id = request.POST['parent_comment']

            if parent_comment_id == '':
                parent_comment_id = None

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO comment (id, body_text, creation_date, parent_comment_id, post_id, user_id) "
                    "VALUES (nextval('comment_id_seq'), %s, now(), %s, %s, %s)",
                    [body_text, parent_comment_id, post_id, user.id])

            return redirect('/post/'+post_id+'#new_comment')

    return redirect('post', post_id)


def edit_comment_post(request, post_id):

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():

            body_text = request.POST['body_text']
            comment_id = request.POST['comment_id']

            user = request.user

            comment = Comment.objects.raw('SELECT * '
                                          'FROM comment '
                                          'WHERE id = %s AND user_id = %s', [comment_id, user.id])

            # перевіряємо дозволи - адмін/модератор або власник коментаря
            if user.has_perm('hitchify.change_comment') or comment[0].user_id == user.id:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE comment SET body_text = %s WHERE id = %s",
                        [body_text, comment_id])

                return redirect('/post/'+post_id+'#new_comment')

    return redirect('post', post_id)


def del_comment_post(request, post_id):

    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        user = request.user

        comment = Comment.objects.raw('SELECT * '
                                      'FROM comment '
                                      'WHERE id = %s AND user_id = %s', [comment_id, user.id])

        # перевіряємо дозволи - адмін/модератор або власник коментаря
        if user.has_perm('hitchify.delete_comment') or comment[0].user_id == user.id:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM comment WHERE id = %s",
                    [comment_id])

            return redirect('/post/'+post_id+'#new_comment')

    return redirect('post', post_id)


@permission_required('hitchify.add_country')
def add_country(request):

    if request.method == 'POST':
        form = forms.AddCountryForm(request.POST)
        if form.is_valid():

            country_name = request.POST['country_name']
            short_description = request.POST['short_description']
            national_currency = request.POST['national_currency']

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO country (id, country_name, short_description, national_currency) "
                    "VALUES (nextval('country_id_seq'), %s, %s, %s)",
                    [country_name, short_description, national_currency])

            last_id = Country.objects.latest('id').id

            return redirect('country', last_id)

    return redirect('administration')


@permission_required('hitchify.add_guide')
def add_guide(request):

    if request.method == 'POST':
        form = forms.AddGuideForm(request.POST)
        if form.is_valid():

            title = request.POST['title']
            body_text = request.POST['body_text']
            short_summary = request.POST['short_summary']
            user = request.user

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO guide (id, title, body_text, short_summary, creation_date, user_id) "
                    "VALUES (nextval('guide_id_seq'), %s, %s, %s, now(), %s)",
                    [title, body_text, short_summary, user.id])

            last_id = Guide.objects.latest('id').id

            return redirect('guide', last_id)

    return redirect('administration')


def signup(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # base_user_id = request.user.id
            created_user_username = form.cleaned_data['username']

            with connection.cursor() as cursor:
                cursor.execute('SELECT id '
                               'FROM auth_user '
                               'WHERE username = %s', [created_user_username])
                created_user_id = cursor.fetchone()
                # return photos

            gender = request.POST['gender']
            birth_date = request.POST.get('birth_date')
            res_country = request.POST['res_country']
            res_city = request.POST['res_city']

            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO myuser (id, base_user_id, gender, birth_date, country, city) '
                               'VALUES (nextval(\'myuser_id_seq\'), %s, %s, %s, %s, %s)',
                               [created_user_id, gender, birth_date, res_country, res_city])

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
    else:
        return redirect('map')

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO hitchspot (id, latitude, longitude, description, avg_hitchability, avg_waiting_time, creation_date, last_update, country_id,user_id)"
            " VALUES (nextval('hitchspot_id_seq'), %s, %s, %s, %s, %s, now(), now(), %s, %s)",
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
    countries = Country.objects.raw('SELECT * '
                                    'FROM country '
                                    'ORDER BY country_name ASC')

    context = {
        'choose': 'country',
        'countries': countries
    }

    return render(request, 'countries.html', context=context)


def country(request, country_id):
    country = Country.objects.raw('SELECT * '
                                  'FROM country '
                                  'WHERE id = %s', [country_id])

    context = {
        'choose': 'country',
        'country': country[0]
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
        'guides': guides,
        'choose': 'guide'
    }

    return render(request, 'guides.html', context=context)


def guide(request, guide_id):
    guide = Guide.objects.get(id=guide_id)

    context = {
        'guide': guide,
    }

    return render(request, 'guide.html', context=context)


@permission_required('hitchify.add_country')
def administration(request):
    context = {
        'choose': 'administration',
    }

    return render(request, 'administration.html', context=context)


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
