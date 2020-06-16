from django.urls import path, include
from hitchifyPY import settings
from . import views
from django.contrib.auth import views as authviews
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', authviews.LoginView.as_view(), name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),

    path('countries/', views.countries, name='countries'),
    path('country/<country_id>', views.country, name='country'),
    path('country/<country_id>/posts', views.country, name='country_post'),
    path('country/<country_id>/add_post/', views.add_post, name='add_post'),
    path('country/<country_id>/edit', views.edit_country, name='edit_country'),
    path('add_country/', views.add_country, name='add_country'),

    path('add_language/', views.add_language, name='add_language'),
    path('connect_lang_country/', views.connect_lang_country, name='connect_lang_country'),

    path('hitchspots/', views.hitchspots, name='hitchspots'),
    path('hitchspot/<hitchspot_id>', views.hitchspot, name='hitchspot'),
    path('hitchspot/<hitchspot_id>/add_comment/', views.add_comment_to_hitchspot,
       name='add_comment_to_hitchspot'),
    path('hitchspot/<hitchspot_id>/edit_comment/', views.edit_comment_hitchspot,
       name='edit_comment_hitchspot'),
    path('hitchspot/<hitchspot_id>/del_comment/', views.del_comment_hitchspot,
       name='del_comment_hitchspot'),
    path('hitchspot/<spot_id>/add_feedback/', views.add_feedback_to_spot, name='add_feedback_to_spot'),
    path('hitchspot/<spot_id>/add_photo/', views.add_photo_to_spot, name='add_photo_to_spot'),
    path('hitchspot/<spot_id>/del_photo/<photo_id>', views.del_photo_from_spot, name='del_photo_from_spot'),

    path('forum/', views.forum, name='forum'),

    path('post/<post_id>', views.post, name='post'),
    path('post/<post_id>/like', views.like_post, name='like_post'),
    path('post/<post_id>/edit', views.edit_post, name='edit_post'),
    path('post/<post_id>/add_comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<post_id>/edit_comment/', views.edit_comment_post, name='edit_comment_post'),
    path('post/<post_id>/del_comment/', views.del_comment_post, name='del_comment_post'),
    path('post/<post_id>/add_photo/', views.add_photo_to_post, name='add_photo_to_post'),
    path('post/<post_id>/del_photo/<photo_id>', views.del_photo_from_post, name='del_photo_from_post'),
    path('post/<post_id>/like_post_comment/', views.like_post_comment, name='like_post_comment'),

    path('guides/', views.guides, name='guides'),
    path('guide/<guide_id>', views.guide, name='guide'),
    path('guide/<guide_id>/edit', views.edit_guide, name='edit_guide'),
    path('add_guide/', views.add_guide, name='add_guide'),
    path('guide/<guide_id>/add_photo/', views.add_photo_to_guide, name='add_photo_to_guide'),
    path('guide/<guide_id>/del_photo/<photo_id>', views.del_photo_from_guide, name='del_photo_from_guide'),

    path('guide/<guide_id>/add_suggestion', views.add_suggestion, name='add_suggestion'),
    path('guide/<guide_id>/see_suggestions', views.see_suggestions, name='see_suggestions'),

    path('suggestions/<gf_id>/delete', views.delete_suggestion, name='del_suggestion'),

    path('administration/', views.administration, name='administration'),

    path('map/', views.hitchify_map, name='map'),
    path('map/<country_id>', views.hitchify_map_country, name='map_country'),
    path('map_xml/', views.hitchify_xml, name='map_xml'),
    path('map_xml/<country_id>', views.hitchify_xml_country, name='map_xml_country'),

    path('add_point/', views.add_point, name='add_point'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)