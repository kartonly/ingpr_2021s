from django.urls import path, include
from . import views
from .views import NewsView
from .views import SearchResultsView

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('about/<id>', views.news, name='news'),
    path('events/<id>', views.events, name='events'),
    path('about/<id>/update', views.update_news, name='news_update'),
    path('about/<id>/delete', views.delete_news, name='news_delete'),
    path('concerts', views.concerts, name='concerts'),
    path('show', views.show, name='show'),
    path('profile', views.profile, name='profile'),
    path('create', views.create, name='create'),
    path('news/', NewsView.as_view()),
    path('news/<int:pk>', NewsView.as_view()),
    path('accounts/login/',  include('django.contrib.auth.urls'), name='login'),
    path('accounts/logout/', include('django.contrib.auth.urls'), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('dashboard/', include('dashboard.urls'))
    ]
