from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.AdaptiveThresholding import AdaptiveThresholding

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def adaptivethresholding_view(request):
    clean_media_root()

    template_name = 'modules/thresholding/adaptivethresholding.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def adaptivethresholding_diy_view(request):    
    template_name = 'modules/thresholding/adaptivethresholding.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'adaptivethresholding_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        adaptivethresholding_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(adaptivethresholding_path):
            os.makedirs(adaptivethresholding_path)

        generated_adaptivethresholding_path = uimage_path.replace('input_images', 'output_images')
        generated_adaptivethresholding_fname = generate_filename(uimage_fname, 'adaptivethresholding_')
        generated_adaptivethresholding_url = os.path.join(generated_adaptivethresholding_path, generated_adaptivethresholding_fname)

        blocksize = int(request.POST.get('blocksize'))

        # Generate adaptivethresholding Image
        adaptivethresholding_flt = AdaptiveThresholding(uploaded_image_url, save_to_abs)
        im_dim = adaptivethresholding_flt.get_im_dim()
        adaptivethresholding_flt.generate_adaptivethresholding_image(blocksize)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_adaptivethresholding_url': generated_adaptivethresholding_url,
            "show_lec_form": "false",
            "show_diy_form": "true"
        })

    return render(request, template_name)

def adaptivethresholding_lec_view(request):
    template_name = 'modules/thresholding/adaptivethresholding.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        blocksize_list = request.POST.getlist('blocksize')
        generated_adaptivethresholding_url = list()

        for blocksize in blocksize_list:
            # Generate the output image path
            ADAPTIVETHRESHOLDING_PREFIX = 'adaptivethresholding_' + blocksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, ADAPTIVETHRESHOLDING_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            adaptivethresholding_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(adaptivethresholding_path):
                os.makedirs(adaptivethresholding_path)

            generated_adaptivethresholding_path = uimage_path.replace('input_images', 'output_images')
            generated_adaptivethresholding_fname = generate_filename(uimage_fname, ADAPTIVETHRESHOLDING_PREFIX)

            # Generate ADAPTIVETHRESHOLDING Filtered Image
            adaptivethresholding_flt = AdaptiveThresholding(uploaded_image_url, save_to_abs)
            im_dim = adaptivethresholding_flt.get_im_dim()
            ptime = adaptivethresholding_flt.generate_adaptivethresholding_image(int(blocksize))

            generated_adaptivethresholding_obj = {
                "blocksize": blocksize,
                "url": os.path.join(generated_adaptivethresholding_path, generated_adaptivethresholding_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_adaptivethresholding_url.append(generated_adaptivethresholding_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_adaptivethresholding_url': generated_adaptivethresholding_url,
            "show_lec_form": "true",
            "show_diy_form": "false"
        })

    return render(request, template_name)