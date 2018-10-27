from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from datetime import date
import os

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html
    return render(request, 'index.html')

def image_upload_dirpath(filename):
    PATH_SUFFIX = 'input_images'
    today = date.today()
    today_path = today.strftime("%Y/%m/%d")

    filename = os.path.join(PATH_SUFFIX, today_path, filename)

    return filename

def histogram_plot_view(request):
    template_name = 'modules/histogram/hist-plt.html'
    
    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = image_upload_dirpath(uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)
        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url
        })

    return render(request, template_name)