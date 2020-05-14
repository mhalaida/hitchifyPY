import os

from django.contrib.auth import login as my_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from hitchify.models import Comment, Country, ForumPost, Guide, \
                            GuideFeedback, Hitchspot, Language, \
                            LanguageToCountry, Photo, SpotFeedback, \
                            UserLikedComment, UserLikedForumPost

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
        cursor.execute("INSERT INTO hitchspot (spot_id, latitude, longitude, description, avg_hitchability, avg_waiting_time, creation_date, last_update, country_id,user_id)"
                        " VALUES (nextval('spot_sequence'), %s, %s, %s, %s, %s, now(), now(), %s, %s)", [lt, ln, description, avg_hitchability, avg_waiting_time, country_id, user_id])

    country = Country.objects.get(country_id=country_id)

    context = {
        'country': country,
        'choose': 'map',
    }

    return render(request, 'map_country.html', context = context)


def login(request):

    context = {}

    return render(request, os.path.join(BASE_DIR, 'templates/registration/login.html'), context = context)


def countries(request):

    country = Country.objects.all()    
    
    context = {
        'choose': 'country',
        'country': country,
    }

    return render(request, 'countries.html', context = context)


def country(request, country_id):

    country = Country.objects.get(country_id=country_id)
    
    context = {
        'choose': 'country',
        'country': country        
    }

    return render(request, 'country.html', context = context)


def hitchspots(request):

    hitchspot = Hitchspot.objects.all()

    context = {
        'hitchspot': hitchspot
    }

    return render(request, 'hitchspots.html', context = context)


def forum(request):

    forum = ForumPost.objects.all()

    context = {
        'forum': forum
    }

    return render(request, 'forum.html', context = context)


def post(request, post_id):

    post = ForumPost.objects.get(post_id=post_id)

    context = {
        'post': post
    }

    return render(request, 'post.html', context = context)


def guides(request):

    guides = Guide.objects.all()

    context = {
        'guides': guides
    }

    return render(request, 'guides.html', context = context)


def guide(request):

    context = {}

    return render(request, 'guide.html', context = context)


def hitchify_map(request):

    context = {
        'choose': 'map',
    }

    return render(request, 'map.html', context = context)

def hitchify_map_country(request, country_id):

    country = Country.objects.get(country_id=country_id)

    context = {
        'country': country,
        'choose': 'map',
    }

    return render(request, 'map_country.html', context = context)

def hitchify_xml(request):

    hitchspots = Hitchspot.objects.all()
    
    context = {'hitchspots': hitchspots}
    
    return render(request, 'map_xml.html', context = context, content_type="application/xhtml+xml")

def hitchify_xml_country(request, country_id):

    hitchspots = Hitchspot.objects.raw('SELECT * '
                                       'FROM hitchspot '
                                       'WHERE country_id = %s', [country_id])
    
    context = {'hitchspots': hitchspots}
    
    return render(request, 'map_xml.html', context = context, content_type="application/xhtml+xml")
