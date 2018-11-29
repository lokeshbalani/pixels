from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Laplacian import Laplacian

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def laplacian_filter_view(request):
    clean_media_root()

    template_name = 'modules/derivatives/laplacian.html'
    return render(request, template_name)

def laplacian_filter_lec_view(request):
    template_name = 'modules/derivatives/laplacian.html'

    if request.method == 'POST' and request.FILES['prof_upload_image']:
        uploaded_image = request.FILES['prof_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        ksize_list = request.POST.getlist('ksize')
        generated_laplacian_url = list()

        for ksize in ksize_list:
            # Generate the output image path
            LAPLACIAN_PREFIX = 'laplacian_' + ksize + "_"
            save_to = images_dirpath('output_images', uimage_fname, LAPLACIAN_PREFIX)
            save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

            # Create output_images folder if it DNE
            laplacian_path = get_filename(save_to_abs)[0]
            if not os.path.isdir(laplacian_path):
                os.makedirs(laplacian_path)

            generated_laplacian_path = uimage_path.replace('input_images', 'output_images')
            generated_laplacian_fname = generate_filename(uimage_fname, LAPLACIAN_PREFIX)

            # Generate Laplacian Filtered Image
            laplacian_flt = Laplacian(uploaded_image_url, save_to_abs)
            im_dim = laplacian_flt.get_im_dim()
            ptime = laplacian_flt.generate_laplacian_filtered_image(int(ksize))

            generated_laplacian_obj = {
                "operator": ksize,
                "url": os.path.join(generated_laplacian_path, generated_laplacian_fname),
                "w": im_dim[1],
                "h": im_dim[0],
                "ptime": ptime
            }

            generated_laplacian_url.append(generated_laplacian_obj)

        return render(request, template_name, {
            'lec_uploaded_image_url': uploaded_image_url,
            'lec_generated_laplacian_url': generated_laplacian_url
        })

    return render(request, template_name)