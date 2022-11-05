from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse, Http404

from .models import Circle

# Create your views here.
def drawing(request):
    return render(request, 'drawing.html')

def index(request):
    all_circles_list = Circle.objects.order_by('-draw_date')

    context = {
        'all_circles_list': all_circles_list,
    }

    return render(request, 'index.html', context)

def circle(request, circle_id):
    try:
        circle = Circle.objects.get(pk = circle_id)
    except Circle.DoesNotExist:
        raise Http404("Circle does not exist")

    return render(request, 'circle.html', {'circle': circle})
    
