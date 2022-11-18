from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.http import HttpResponse, Http404, HttpResponseRedirect

from circleScoreApp.forms import circleForm

from .models import Circle
from .utils.circularity import calculateCircularity

from io import BytesIO, StringIO
from PIL import Image
import base64
import re
import datetime
import uuid


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
            image = image.convert("L")
            image.save("black.png")

            # culculate the circularity of the circle
            circularity = calculateCircularity(image)

            # Create a file-like object to upload to the database (not PIL Image)
            # + file name based on time of upload
            image_io = BytesIO()
            image.save(image_io, format='PNG')
            file_name = str(uuid.uuid4().hex)
            image_file = ContentFile(image_io.getvalue(), name=(file_name + ".png"))

            # create new circle
            new_circle = Circle(artist_name = artist_name, circle = image_file, circularity=circularity)

            # save the circle 
            new_circle.save()
            
            return redirect("circle", new_circle.id)
        
        else:
            return redirect("drawing")

def index(request):
    all_circles_list = Circle.objects.order_by('-draw_date')
    drawn_today = Circle.objects.filter(draw_date__date= datetime.date.today())
    best_today = drawn_today.order_by('-circularity').first()
    # best_today = drawn_today.order_by('circularity').first()

    context = {
        'all_circles_list': all_circles_list,
        'best_today': best_today,
    }

    return render(request, 'circleScoreApp/index.html', context)

def circle(request, circle_id):
    try:
        circle = Circle.objects.get(pk = circle_id)
    except Circle.DoesNotExist:
        raise Http404("Circle does not exist")

    return render(request, 'circleScoreApp/circle.html', {'circle': circle})
    
