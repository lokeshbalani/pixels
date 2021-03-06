from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Sobel import Sobel

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def sobel_filter_view(request):
    clean_media_root()

    template_name = 'modules/derivatives/sobel.html'
    return render(request, template_name)

def sobel_filter_lec_view(request):
    template_name = 'modules/derivatives/sobel.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_sobel_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            SOBEL_PREFIX = 'sobel_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, SOBEL_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            sobel_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(sobel_path):
                os.makedirs(sobel_path)

            generated_sobel_path = uimage_path.replace('input_images', 'output_images')
            generated_sobel_fname = generate_filename(uimage_fname, SOBEL_PREFIX)

            # Generate Sobel Filtered Image
            sobel_flt = Sobel(uploaded_image_url, save_to_abs)
            im_dim = sobel_flt.get_im_dim()
            ptime = sobel_flt.generate_sobel_filtered_image(int(ksize))

            generated_sobel_obj = {
                "operator": ksize,
                "url": os.path.join(generated_sobel_path, generated_sobel_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_sobel_url.append(generated_sobel_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_sobel_url': generated_sobel_url
        })

    return render(request, template_name)