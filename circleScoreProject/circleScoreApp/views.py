from django.shortcuts import render, redirect
from django.template import loader

from django.http import HttpResponse, Http404, HttpResponseRedirect
from circleScoreApp.forms import circleForm

from .models import Circle
from .utils.circularity import calculateCircularity

from io import BytesIO, StringIO
from binascii import a2b_base64
from PIL import Image
import base64
import re



# Create your views here.
def drawing(request):

    if (request.method == 'GET'):
        form = circleForm()
        context = {'form':form}
        return render(request, 'circleScoreApp/drawing.html', context)
        
    elif (request.method == 'POST'):
        form = circleForm(request.POST)

        if form.is_valid():
            artist_name = form.cleaned_data['artist_name']
            canvas_data = request.POST['image']
            # image_width = int(request.POST['image_width'])
            # image_height = int(request.POST['image_height'])

            # decode the canvas data given in the POST
            base64_data = re.sub("^data:image/png;base64,", "", canvas_data)
            binary_data = base64.b64decode(base64_data)
            image_data = BytesIO(binary_data)
            image = Image.open(image_data)

            # convert from x-channel to 1-channel grayscale
            image = image.convert("1")

            image.save("testestest.png")
            circ = calculateCircularity(image)

            new_circle = Circle(artist_name = artist_name, circle = image, circularity=circ)
            new_circle.save()
            
            return redirect("index")
        
        else:
            print("form not valid.")
            return redirect("drawing")

def index(request):
    all_circles_list = Circle.objects.order_by('-draw_date')

    context = {
        'all_circles_list': all_circles_list,
    }

    return render(request, 'circleScoreApp/index.html', context)

def circle(request, circle_id):
    try:
        circle = Circle.objects.get(pk = circle_id)
    except Circle.DoesNotExist:
        raise Http404("Circle does not exist")

    return render(request, 'circleScoreApp/circle.html', {'circle': circle})
    
