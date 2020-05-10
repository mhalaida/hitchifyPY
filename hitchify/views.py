from django.shortcuts import render
from hitchify.models import Comment, Country, ForumPost, Guide, \
                            GuideFeedback, Hitchspot, Language, \
                            LanguageToCountry, Photo, SpotFeedback, \
                            UserLikedComment, UserLikedForumPost

# Create your views here.

def index(request):

    num_spots = Hitchspot.objects.all().count()
    num_forum_posts = ForumPost.objects.all().count()
    num_guides = Guide.objects.all().count()

    context = {
        'num_spots': num_spots,
        'num_forum_posts': num_forum_posts,
        'num_guides': num_guides
    }

    return render(request, 'index.html', context = context)

def login(request):

    context = {

    }

    return render(request, 'login.html', context = context)


def countries(request):

    country = Country.objects.all()    
    
    context = {
        'country': country,
    }

    return render(request, 'countries.html', context = context)

def country(request, country_id):

    country = Country.objects.get(country_id=country_id)
    
    context = {
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

def post(request):

    context = {
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

def map(request):

    context = {}

    return render(request, 'map.html', context = context)
