from django.urls import path, include
from hitchifyPY import settings
from . import views
from django.contrib.auth import views as authviews
from django.conf.urls.static import static


urlpatterns = [
    path('', authviews.LoginView.as_view(), name='login'),
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('countries/', views.countries, name='countries'),
    path('country/<country_id>', views.country, name='country'),
    path('hitchspots/', views.hitchspots, name='hitchspots'),
    path('forum/', views.forum, name='forum'),
    path('post/', views.post, name='post'),
    path('guides/', views.guides, name='guides'),
    path('guide/', views.guide, name='guide'),
    path('map/', views.hitchify_map, name='map'),

    # path('accounts/', include('django.contrib.auth.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)