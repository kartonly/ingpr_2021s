from django.urls import path
from . import views
from .views import NewsView

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('concerts', views.concerts, name='concerts'),
    path('show', views.show, name='show'),
    path('create', views.create, name='create'),
    path('news/', NewsView.as_view()),
    path('news/<int:pk>', NewsView.as_view())
    ]
