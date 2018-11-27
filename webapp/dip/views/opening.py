from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Opening import Opening

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def opening_filter_view(request):
    clean_media_root()

    template_name = 'modules/morphological/opening.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def opening_filter_diy_view(request):    
    template_name = 'modules/morphological/opening.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'opening_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        opening_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(opening_path):
            os.makedirs(opening_path)

        generated_opening_path = uimage_path.replace('input_images', 'output_images')
        generated_opening_fname = generate_filename(uimage_fname, 'opening_')
        generated_opening_url = os.path.join(generated_opening_path, generated_opening_fname)

        ksize = int(request.POST.get('ksize'))

        # Generate Opening Filtered Image
        opening_flt = Opening(uploaded_image_url, save_to_abs)
        im_dim = opening_flt.get_im_dim()
        opening_flt.generate_opening_filtered_image(ksize)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_opening_url': generated_opening_url,
            "show_lec_form": "false",
            "show_diy_form": "true"
        })

    return render(request, template_name)

def opening_filter_lec_view(request):
    template_name = 'modules/morphological/opening.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_opening_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            OPENING_PREFIX = 'opening_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, OPENING_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            opening_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(opening_path):
                os.makedirs(opening_path)

            generated_opening_path = uimage_path.replace('input_images', 'output_images')
            generated_opening_fname = generate_filename(uimage_fname, OPENING_PREFIX)

            # Generate Opening Filtered Image
            opening_flt = Opening(uploaded_image_url, save_to_abs)
            im_dim = opening_flt.get_im_dim()
            ptime = opening_flt.generate_opening_filtered_image(int(ksize))

            generated_opening_obj = {
                "ksize": ksize,
                "url": os.path.join(generated_opening_path, generated_opening_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_opening_url.append(generated_opening_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_opening_url': generated_opening_url,
            "show_lec_form": "true",
            "show_diy_form": "false"
        })

    return render(request, template_name)