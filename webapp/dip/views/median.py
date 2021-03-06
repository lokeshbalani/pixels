from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Median import Median

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def median_filter_view(request):
    clean_media_root()

    template_name = 'modules/spatial_filters/median.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def median_filter_diy_view(request):    
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

        ksize = int(request.POST.get('ksize'))

        # Generate Median Filtered Image
        median_flt = Median(uploaded_image_url, save_to_abs)
        im_dim = median_flt.get_im_dim()
        ptime = median_flt.generate_median_filtered_image(ksize)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_median_url': generated_median_url,
            "show_lec_form": "false",
            "show_diy_form": "true",
            "im_width": im_dim[1],
            "im_height": im_dim[0],
            "ptime": ptime,
            "ksize": ksize
        })

    return render(request, template_name)

def median_filter_lec_view(request):
    template_name = 'modules/spatial_filters/median.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_median_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            MEDIAN_PREFIX = 'median_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, MEDIAN_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            median_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(median_path):
                os.makedirs(median_path)

            generated_median_path = uimage_path.replace('input_images', 'output_images')
            generated_median_fname = generate_filename(uimage_fname, MEDIAN_PREFIX)

            # Generate Median Filtered Image
            median_flt = Median(uploaded_image_url, save_to_abs)
            im_dim = median_flt.get_im_dim()
            ptime = median_flt.generate_median_filtered_image(int(ksize))

            generated_median_obj = {
                "ksize": ksize,
                "url": os.path.join(generated_median_path, generated_median_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_median_url.append(generated_median_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_median_url': generated_median_url,
            "show_lec_form": "true",
            "show_diy_form": "false"
        })

    return render(request, template_name)