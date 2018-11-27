from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Dilation import Dilation

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def dilation_filter_view(request):
    clean_media_root()

    template_name = 'modules/morphological/dilation.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def dilation_filter_diy_view(request):    
    template_name = 'modules/morphological/dilation.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'dilation_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        dilation_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(dilation_path):
            os.makedirs(dilation_path)

        generated_dilation_path = uimage_path.replace('input_images', 'output_images')
        generated_dilation_fname = generate_filename(uimage_fname, 'dilation_')
        generated_dilation_url = os.path.join(generated_dilation_path, generated_dilation_fname)

        ksize = int(request.POST.get('ksize'))

        # Generate Dilation Filtered Image
        dilation_flt = Dilation(uploaded_image_url, save_to_abs)
        im_dim = dilation_flt.get_im_dim()
        dilation_flt.generate_dilation_filtered_image(ksize)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_dilation_url': generated_dilation_url,
            "show_lec_form": "false",
            "show_diy_form": "true"
        })

    return render(request, template_name)

def dilation_filter_lec_view(request):
    template_name = 'modules/morphological/dilation.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_dilation_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            DILATION_PREFIX = 'dilation_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, DILATION_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            dilation_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(dilation_path):
                os.makedirs(dilation_path)

            generated_dilation_path = uimage_path.replace('input_images', 'output_images')
            generated_dilation_fname = generate_filename(uimage_fname, DILATION_PREFIX)

            # Generate Dilation Filtered Image
            dilation_flt = Dilation(uploaded_image_url, save_to_abs)
            im_dim = dilation_flt.get_im_dim()
            ptime = dilation_flt.generate_dilation_filtered_image(int(ksize))

            generated_dilation_obj = {
                "ksize": ksize,
                "url": os.path.join(generated_dilation_path, generated_dilation_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_dilation_url.append(generated_dilation_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_dilation_url': generated_dilation_url,
            "show_lec_form": "true",
            "show_diy_form": "false"
        })

    return render(request, template_name)