from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def drawingPage(request):
    return HttpResponse("Draw a circle!")
