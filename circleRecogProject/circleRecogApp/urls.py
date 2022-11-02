from django.urls import path

from . import views

urlpatterns = {
    path('', views.drawingPage, name = "drawing_page")
}