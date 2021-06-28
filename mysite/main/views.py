from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework.generics import get_object_or_404
from tablib.packages.dbfpy import record

from .models import News, SoldTickets
from .models import Event
from .models import Tickets
from .models import User
from .forms import NewsForm
from .models import TicketsCount
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from .serializers import NewsSerializer
from django import template
from django.contrib.auth.models import Group

register = template.Library()


def index(request):
    event = Event.objects.all()
    ticket = Tickets.objects.values_list('Price')
    n = ticket.order_by('Price').first()

    return render(request, 'main/index.html', {'event':event, 'ticket':ticket, 'n':n})


def about(request):
    n = 0;
    if request.method=='POST':
        n = n+1;

    if n % 2==0:
        news = News.objects.order_by('id')
    else:
        news = News.objects.order_by('-id')

    return render(request, 'main/about.html', {'news':news})


def news(request, id):
    context={}

    # add the dictionary during initialization
    context["data"] = News.objects.get(id=id)

    return render(request, "detail_news_view.html", context)


def events(request, id):
    context={}

    # add the dictionary during initialization
    context["data"] = Event.objects.get(id=id)

    return render(request, "detail_events_view.html", context)


def update_news(request, id):
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(News, id=id)

    # pass the object as instance in form
    form = NewsForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/about/"+id)

    context["form"] = form

    return render(request, "update_news.html", context)


def delete_news(request, id):
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(News, id=id)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/about")

    return render(request, "delete_news.html", context)


def concerts(request):
    event = Event.objects.filter(TypeId=1)
    count = Event.objects.filter(TypeId=1).count()
    return render(request, 'main/concerts.html', {'event':event, 'count':count})


def other(request):
        event = Event.objects.exclude(TypeId=1).exclude(TypeId=2)
        count = Event.objects.exclude(TypeId=1).exclude(TypeId=2).count()
        return render(request, 'main/other.html', {'event':event, 'count':count})


def profile(request):
    if SoldTickets.objects.filter(Buyer=request.user.id).exists():
        ticket_all = SoldTickets.objects.filter(Buyer=request.user.id)
        add = "Ждём вас на мероприятиях!"
        return render(request, 'main/profile.html', {'ticket':ticket_all, 'add':add})
    else:
        add = "У вас нет билетов :("
        return render(request, 'main/profile.html', {'add':add})


def logout(request):
    return render(request, 'registration/logged_out.html')


def create(request):
    if request.method == 'POST':
        forms = NewsForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('about')


    form = NewsForm()
    context = {
         'form': form,
    }
    return render(request, 'main/create.html', context)


def show(request):
    event = Event.objects.filter(TypeId=2)
    count = Event.objects.filter(TypeId=2).count()
    return render(request, 'main/show.html', {'event':event, 'count':count})


def allevent(request):
    event = Event.objects.all()
    return render(request, 'main/index.html', {'event':event})


class NewsView(APIView):
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response({"news": serializer.data})

    def post(self, request):
        news = request.data.get("news")
        # Create an article from the above data
        serializer = NewsSerializer(data=news)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "News '{}' created successfully".format(article_saved.Title)})

    def put(self, request, pk):
        saved_news = get_object_or_404(News.objects.all(), pk=pk)
        data = request.data.get('news')
        serializer = NewsSerializer(instance=saved_news, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            news_saved = serializer.save()
        return Response({
            "success": "News '{}' updated successfully".format(news_saved.Title)
        })

    def delete(self, request, pk):
        # Get object with this pk
        news = get_object_or_404(News.objects.all(), pk=pk)
        news.delete()
        return Response({
            "message": "News with id `{}` has been deleted.".format(pk)}, status=204)


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


def is_in_groups(user):
    return user.groups.filter(name__in=['Admin', 'Manager']).exists()


class SearchResultsView(ListView):
    model = Event
    template_name = 'main/search_results.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Event.objects.filter(
            Q(Name__icontains=query) | Q(About__icontains=query)
        )
        return object_list



