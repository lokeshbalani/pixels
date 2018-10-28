from django.shortcuts import render, redirect
from django.views import generic
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from datetime import date
import os
from dip.py_modules.Histogram import Histogram

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html
    return render(request, 'index.html')

def images_dirpath(suffix, filename, prefix=None):
    PATH_SUFFIX = suffix 

    if prefix is not None:
        PATH_PREFIX = prefix 
    else:
        PATH_PREFIX = ''

    today = date.today()
    today_path = today.strftime("%Y/%m/%d")

    filename = os.path.join(PATH_SUFFIX, today_path, PATH_PREFIX, filename)

    return filename

def histogram_plot_view(request):
    template_name = 'modules/histogram/hist-plt.html'
    
    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        # Generate Histogram
        histr = Histogram(uploaded_image_url).generate_histogram()

        save_to = images_dirpath('output_images', uploaded_image.name, 'hist_')
        fname = fs.save(save_to, histr)
        uploaded_hist_url = fs.url(fname)

        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url,
            'uploaded_hist_url': uploaded_hist_url
        })

    return render(request, template_name)