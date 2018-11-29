from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Averaging import Averaging

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def averaging_filter_view(request):
    clean_media_root()

    template_name = 'modules/spatial_filters/averaging.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def averaging_filter_diy_view(request):    
    template_name = 'modules/spatial_filters/averaging.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'averaging_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        averaging_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(averaging_path):
            os.makedirs(averaging_path)

        generated_averaging_path = uimage_path.replace('input_images', 'output_images')
        generated_averaging_fname = generate_filename(uimage_fname, 'averaging_')
        generated_averaging_url = os.path.join(generated_averaging_path, generated_averaging_fname)

        ksize = int(request.POST.get('ksize'))

        # Generate Averaging Filtered Image
        averaging_flt = Averaging(uploaded_image_url, save_to_abs)
        im_dim = averaging_flt.get_im_dim()
        ptime = averaging_flt.generate_averaging_filtered_image(ksize)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_averaging_url': generated_averaging_url,
            "show_lec_form": "false",
            "show_diy_form": "true",
            "im_width": im_dim[1],
            "im_height": im_dim[0],
            "ptime": ptime,
            "ksize": ksize
        })

    return render(request, template_name)

def averaging_filter_lec_view(request):
    template_name = 'modules/spatial_filters/averaging.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_averaging_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            AVERAGING_PREFIX = 'averaging_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, AVERAGING_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            averaging_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(averaging_path):
                os.makedirs(averaging_path)

            generated_averaging_path = uimage_path.replace('input_images', 'output_images')
            generated_averaging_fname = generate_filename(uimage_fname, AVERAGING_PREFIX)

            # Generate Averaging Filtered Image
            averaging_flt = Averaging(uploaded_image_url, save_to_abs)
            im_dim = averaging_flt.get_im_dim()
            ptime = averaging_flt.generate_averaging_filtered_image(int(ksize))

            generated_averaging_obj = {
                "ksize": ksize,
                "url": os.path.join(generated_averaging_path, generated_averaging_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_averaging_url.append(generated_averaging_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_averaging_url': generated_averaging_url,
            "show_lec_form": "true",
            "show_diy_form": "false"
        })

    return render(request, template_name)