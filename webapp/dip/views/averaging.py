from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Averaging import Averaging

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def avg_filter_view(request):
    clean_media_root()

    template_name = 'modules/spatial_filters/averaging.html'
    return render(request, template_name)

def avg_filter_diy_view(request):    
    template_name = 'modules/spatial_filters/averaging.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'avg_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        avg_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(avg_path):
            os.makedirs(avg_path)

        generated_avg_path = uimage_path.replace('input_images', 'output_images')
        generated_avg_fname = generate_filename(uimage_fname, 'avg_')
        generated_avg_url = os.path.join(generated_avg_path, generated_avg_fname)

        ksize = int(request.POST.get('ksize'))

        # Generate Average Filtered Image
        Averaging(uploaded_image_url, save_to_abs).generate_avg_filtered_image(ksize)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_avg_url': generated_avg_url
        })

    return render(request, template_name)

def avg_filter_lec_view(request):
    template_name = 'modules/spatial_filters/averaging.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_avg_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            AVG_PREFIX = 'avg_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, AVG_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            avg_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(avg_path):
                os.makedirs(avg_path)

            generated_avg_path = uimage_path.replace('input_images', 'output_images')
            generated_avg_fname = generate_filename(uimage_fname, AVG_PREFIX)
            generated_avg_obj = {
                "ksize": ksize,
                "url": os.path.join(generated_avg_path, generated_avg_fname)
            }

            generated_avg_url.append(generated_avg_obj)

            # Generate Average Filtered Image
            Averaging(uploaded_image_url, save_to_abs).generate_avg_filtered_image(int(ksize))

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_avg_url': generated_avg_url
        })

    return render(request, template_name)