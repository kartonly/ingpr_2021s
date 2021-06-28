from django.http import JsonResponse
from django.shortcuts import render
from main.models import Tickets
from django.core import serializers

def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})

def pivot_data(request):
    dataset = Tickets.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
