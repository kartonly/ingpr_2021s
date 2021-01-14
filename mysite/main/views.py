from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from .models import News
from .models import Event
from .models import Tickets
from .forms import NewsForm
from .models import TicketsCount
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from .serializers import NewsSerializer


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


def concerts(request):
    event = Event.objects.filter(TypeId=1)
    return render(request, 'main/concerts.html', {'event':event})


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
    return render(request, 'main/show.html', {'event':event})


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




