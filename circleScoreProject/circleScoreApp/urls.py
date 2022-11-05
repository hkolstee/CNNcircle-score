from django.urls import path

from . import views

urlpatterns = [
    path('', views.drawing, name = 'drawing'),
    path('index/', views.index, name = 'index'),
    path('index/<int:circle_id>/', views.circle, name = 'circle'),
]