from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Histogram import Histogram

from .helpers import get_filename, images_dirpath, generate_filename

def histogram_plot_view(request):
    template_name = 'modules/histogram/hist-plt.html'
    
    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'histogram_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        hist_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(hist_path):
            os.makedirs(hist_path)

        generated_hist_path = uimage_path.replace('input_images', 'output_images')
        generated_hist_fname = generate_filename(uimage_fname, 'histogram_')
        generated_hist_url = os.path.join(generated_hist_path, generated_hist_fname)

        # Generate Histogram
        Histogram(uploaded_image_url, save_to_abs).generate_histogram()

        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url,
            'generated_hist_url': generated_hist_url
        })

    return render(request, template_name)