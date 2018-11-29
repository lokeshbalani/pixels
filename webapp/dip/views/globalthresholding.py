from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.GlobalThresholding import GlobalThresholding

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def globalthresholding_view(request):
    clean_media_root()

    template_name = 'modules/thresholding/globalthresholding.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def globalthresholding_diy_view(request):    
    template_name = 'modules/thresholding/globalthresholding.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'globalthresholding_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        globalthresholding_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(globalthresholding_path):
            os.makedirs(globalthresholding_path)

        generated_globalthresholding_path = uimage_path.replace('input_images', 'output_images')
        generated_globalthresholding_fname = generate_filename(uimage_fname, 'globalthresholding_')
        generated_globalthresholding_url = os.path.join(generated_globalthresholding_path, generated_globalthresholding_fname)

        threshold = int(request.POST.get('threshold'))

        # Generate globalthresholding Image
        globalthresholding_flt = GlobalThresholding(uploaded_image_url, save_to_abs)
        im_dim = globalthresholding_flt.get_im_dim()
        ptime = globalthresholding_flt.generate_globalthresholding_image(threshold)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_globalthresholding_url': generated_globalthresholding_url,
            "show_lec_form": "false",
            "show_diy_form": "true",
            "im_width": im_dim[1],
            "im_height": im_dim[0],
            "ptime": ptime,
            "threshold": threshold
        })

    return render(request, template_name)

def globalthresholding_lec_view(request):
    template_name = 'modules/thresholding/globalthresholding.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        threshold_list = request.POST.getlist('threshold')
        generated_globalthresholding_url = list()

        for threshold in threshold_list:
            # Generate the output image path
            GLOBALTHRESHOLDING_PREFIX = 'globalthresholding_' + threshold + "_"
            save_to = images_dirpath('output_images', uimage_fname, GLOBALTHRESHOLDING_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            globalthresholding_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(globalthresholding_path):
                os.makedirs(globalthresholding_path)

            generated_globalthresholding_path = uimage_path.replace('input_images', 'output_images')
            generated_globalthresholding_fname = generate_filename(uimage_fname, GLOBALTHRESHOLDING_PREFIX)

            # Generate GLOBALTHRESHOLDING Filtered Image
            globalthresholding_flt = GlobalThresholding(uploaded_image_url, save_to_abs)
            im_dim = globalthresholding_flt.get_im_dim()
            ptime = globalthresholding_flt.generate_globalthresholding_image(int(threshold))

            generated_globalthresholding_obj = {
                "threshold": threshold,
                "url": os.path.join(generated_globalthresholding_path, generated_globalthresholding_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_globalthresholding_url.append(generated_globalthresholding_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_globalthresholding_url': generated_globalthresholding_url,
            "show_lec_form": "true",
            "show_diy_form": "false"
        })

    return render(request, template_name)