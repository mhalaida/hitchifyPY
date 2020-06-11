from django.urls import path, include
from hitchifyPY import settings
from . import views
from django.contrib.auth import views as authviews
from django.conf.urls.static import static


urlpatterns = [
    path('', authviews.LoginView.as_view(), name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('countries/', views.countries, name='countries'),
    path('country/<country_id>', views.country, name='country'),
    path('country/<country_id>/posts', views.country, name='country_post'),
    path('hitchspots/', views.hitchspots, name='hitchspots'),
    path('forum/', views.forum, name='forum'),
    path('post/<post_id>', views.post, name='post'),
    path('post/<post_id>new_comment', views.post, name='post_new_comment'),
    path('country/<country_id>/add_post/', views.add_post, name='add_post'),
    path('post/<post_id>/like', views.like_post, name='like_post'),
    path('post/<post_id>/add_comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('guides/', views.guides, name='guides'),
    path('guide/<guide_id>', views.guide, name='guide'),
    path('map/', views.hitchify_map, name='map'),
    path('map/<country_id>', views.hitchify_map_country, name='map_country'),
    path('map_xml/', views.hitchify_xml, name='map_xml'),
    path('map_xml/<country_id>', views.hitchify_xml_country, name='map_xml_country'),
    path('add_point/', views.add_point, name='add_point'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)