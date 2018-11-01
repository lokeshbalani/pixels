from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Median import Median

from .helpers import get_filename, images_dirpath, generate_filename

def median_filter_view(request):
    template_name = 'modules/spatial_filters/median.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'median_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        median_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(median_path):
            os.makedirs(median_path)

        generated_median_path = uimage_path.replace('input_images', 'output_images')
        generated_median_fname = generate_filename(uimage_fname, 'median_')
        generated_median_url = os.path.join(generated_median_path, generated_median_fname)

        # Generate Median Filtered Image
        Median(uploaded_image_url, save_to_abs).generate_median_filtered_image()

        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url,
            'generated_median_url': generated_median_url
        })

    return render(request, template_name)