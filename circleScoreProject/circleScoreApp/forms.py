from django.forms import ModelForm
from circleScoreApp.models import Circle
from django import forms

class circleForm(ModelForm):
    class Meta:
        model = Circle
        fields = ['artist_name']

        
