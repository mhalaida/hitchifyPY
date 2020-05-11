from django.urls import path, include
from hitchifyPY import settings
from . import views
from django.contrib.auth import views as authviews
from django.conf.urls.static import static


urlpatterns = [
    path('', authviews.LoginView.as_view(), name='index'),
    # path('login/', authviews.LoginView.as_view(), name='login'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('countries/', views.countries, name='countries'),
    path('country/<country_id>', views.country, name='country'),
    path('hitchspots/', views.hitchspots, name='hitchspots'),
    path('forum/', views.forum, name='forum'),
    path('post/', views.post, name='post'),
    path('guides/', views.guides, name='guides'),
    path('guide/', views.guide, name='guide'),
    path('map/', views.hitchify_map, name='map'),
    path('map_xml/', views.hitchify_xml, name='map_xml'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)