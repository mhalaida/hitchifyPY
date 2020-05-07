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
