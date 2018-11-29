from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.ConnectedComponents import ConnectedComponents

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def connected_components_view(request):
    clean_media_root()

    template_name = 'modules/morphological/connected-components.html'
    return render(request, template_name, {
        "show_lec_form": "true",
        "show_diy_form": "true"
    })

def connected_components_diy_view(request):
    template_name = 'modules/morphological/connected-components.html'
    
    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        cc_save_to = images_dirpath('output_images', uimage_fname, 'cc_')
        cc_save_to_abs = os.path.join(settings.MEDIA_ROOT, cc_save_to)

        # Create output_images folder if it DNE
        cc_path = get_filename(cc_save_to_abs)[0]

        if not os.path.isdir(cc_path):
            os.makedirs(cc_path)

        generated_oim_path = uimage_path.replace('input_images', 'output_images')
        generated_cc_fname = generate_filename(uimage_fname, 'cc_')
        generated_cc_url = os.path.join(generated_oim_path, generated_cc_fname)

        connectivity = int(request.POST.get('connectivity'))

        cc_labelling = ConnectedComponents(uploaded_image_url, cc_save_to_abs)
        ccim_dim = cc_labelling.get_im_dim()
        ccptime = cc_labelling.generate_cc_label_image(connectivity)
        
        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url,
            'generated_cc_url': generated_cc_url,
            "show_lec_form": "false",
            "show_diy_form": "true",
            "ccim_width": ccim_dim[1],
            "ccim_height": ccim_dim[0],
            "ccptime": ccptime,
            "connectivity": connectivity
        })

    return render(request, template_name)

