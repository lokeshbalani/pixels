from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Bilateral import Bilateral

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def bilateral_filter_view(request):
    clean_media_root()

    template_name = 'modules/spatial_filters/bilateral.html'
    return render(request, template_name)

def bilateral_filter_diy_view(request):    
    template_name = 'modules/spatial_filters/bilateral.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'bilateral_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        bilateral_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(bilateral_path):
            os.makedirs(bilateral_path)

        generated_bilateral_path = uimage_path.replace('input_images', 'output_images')
        generated_bilateral_fname = generate_filename(uimage_fname, 'bilateral_')
        generated_bilateral_url = os.path.join(generated_bilateral_path, generated_bilateral_fname)

        ksize      = int(request.POST.get('ksize'))
        sigmaColor = int(request.POST.get('sigmaColor'))
        sigmaSpace = int(request.POST.get('sigmaSpace'))

        # Generate Bilateral Filtered Image
        Bilateral(uploaded_image_url, save_to_abs).generate_bilateral_filtered_image(ksize, sigmaColor, sigmaSpace)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_bilateral_url': generated_bilateral_url
        })

    return render(request, template_name)

def bilateral_filter_lec_view(request):
    template_name = 'modules/spatial_filters/bilateral.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_bilateral_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            BILATERAL_PREFIX = 'bilateral_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, BILATERAL_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            bilateral_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(bilateral_path):
                os.makedirs(bilateral_path)

            generated_bilateral_path = uimage_path.replace('input_images', 'output_images')
            generated_bilateral_fname = generate_filename(uimage_fname, BILATERAL_PREFIX)
            generated_bilateral_obj = {
                "ksize": ksize,
                "url": os.path.join(generated_bilateral_path, generated_bilateral_fname)
            }

            generated_bilateral_url.append(generated_bilateral_obj)

            # Generate Bilateral Filtered Image
            Bilateral(uploaded_image_url, save_to_abs).generate_bilateral_filtered_image(int(ksize))

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_bilateral_url': generated_bilateral_url
        })

    return render(request, template_name)