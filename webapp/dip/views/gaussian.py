from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Gaussian import Gaussian

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def gaussian_filter_view(request):
    clean_media_root()

    template_name = 'modules/spatial_filters/gaussian.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def gaussian_filter_diy_view(request):    
    template_name = 'modules/spatial_filters/gaussian.html'

    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'gaussian_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        gaussian_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(gaussian_path):
            os.makedirs(gaussian_path)

        generated_gaussian_path = uimage_path.replace('input_images', 'output_images')
        generated_gaussian_fname = generate_filename(uimage_fname, 'gaussian_')
        generated_gaussian_url = os.path.join(generated_gaussian_path, generated_gaussian_fname)

        ksize = int(request.POST.get('ksize'))
        sigma = int(request.POST.get('sigma'))        

        # Generate Gaussian Filtered Image
        gaussian_flt = Gaussian(uploaded_image_url, save_to_abs)
        im_dim = gaussian_flt.get_im_dim()
        ptime = gaussian_flt.generate_gaussian_filtered_image(ksize, sigma)

        return render(request, template_name, {
            'diy_uploaded_image_url': uploaded_image_url,
            'diy_generated_gaussian_url': generated_gaussian_url,
            "show_lec_form": "false",
            "show_diy_form": "true",
            "im_width": im_dim[1],
            "im_height": im_dim[0],
            "ptime": ptime,
            "ksize": ksize,
            "sigma": sigma
        })

    return render(request, template_name)

def gaussian_filter_lec_view(request):
    template_name = 'modules/spatial_filters/gaussian.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        sigma = int(request.POST.get('sigma'))          
        generated_gaussian_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            GAUSSIAN_PREFIX = 'gaussian_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, GAUSSIAN_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            gaussian_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(gaussian_path):
                os.makedirs(gaussian_path)

            generated_gaussian_path = uimage_path.replace('input_images', 'output_images')
            generated_gaussian_fname = generate_filename(uimage_fname, GAUSSIAN_PREFIX)

            # Generate Gaussian Filtered Image
            gaussian_flt = Gaussian(uploaded_image_url, save_to_abs)
            im_dim = gaussian_flt.get_im_dim()
            ptime = gaussian_flt.generate_gaussian_filtered_image(int(ksize), sigma)

            generated_gaussian_obj = {
                "ksize": ksize,
                "url": os.path.join(generated_gaussian_path, generated_gaussian_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime,
                "sigma": sigma
            }

            generated_gaussian_url.append(generated_gaussian_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_gaussian_url': generated_gaussian_url,
            "show_lec_form": "true",
            "show_diy_form": "false"
        })

    return render(request, template_name)