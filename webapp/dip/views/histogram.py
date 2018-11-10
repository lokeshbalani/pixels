from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from dip.py_modules.Histogram import Histogram

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def histogram_plot_view(request):
    clean_media_root()
    template_name = 'modules/histogram/hist-plt.html'
    
    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        save_to = images_dirpath('output_images', uimage_fname, 'histogram_')
        save_to_abs = os.path.join(settings.MEDIA_ROOT, save_to)

        # Create output_images folder if it DNE
        hist_path = get_filename(save_to_abs)[0]
        if not os.path.isdir(hist_path):
            os.makedirs(hist_path)

        generated_hist_path = uimage_path.replace('input_images', 'output_images')
        generated_hist_fname = generate_filename(uimage_fname, 'histogram_')
        generated_hist_url = os.path.join(generated_hist_path, generated_hist_fname)

        histogram_type = request.POST.get('histogram_type')

        # Generate Histogram
        Histogram(uploaded_image_url, save_to_abs).generate_histogram(histogram_type)

        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url,
            'generated_hist_url': generated_hist_url
        })

    return render(request, template_name)

def histogram_eq_view(request):
    clean_media_root()
    template_name = 'modules/histogram/hist-eq.html'
    
    if request.method == 'POST' and request.FILES['usr_upload_image']:
        uploaded_image = request.FILES['usr_upload_image']
        fs = FileSystemStorage()
        upload_to = images_dirpath('input_images', uploaded_image.name)
        filename = fs.save(upload_to, uploaded_image)
        uploaded_image_url = fs.url(filename)

        uimage_path, uimage_fname = get_filename(uploaded_image_url)

        # Generate the output image path
        hist_save_to = images_dirpath('output_images', uimage_fname, 'histogram_')
        hist_save_to_abs = os.path.join(settings.MEDIA_ROOT, hist_save_to)
        eqim_save_to = images_dirpath('output_images', uimage_fname, 'eqim_')
        eqim_save_to_abs = os.path.join(settings.MEDIA_ROOT, eqim_save_to)
        hist_eqim_save_to = images_dirpath('output_images', uimage_fname, 'histogram_eqim_')
        hist_eqim_save_to_abs = os.path.join(settings.MEDIA_ROOT, hist_eqim_save_to)
        cnvtim_save_to = images_dirpath('output_images', uimage_fname, 'convert_im_')
        cnvtim_save_to_abs = os.path.join(settings.MEDIA_ROOT, cnvtim_save_to)
        hist_cnvtim_save_to = images_dirpath('output_images', uimage_fname, 'histogram_cnvtim_')
        hist_cnvtim_save_to_abs = os.path.join(settings.MEDIA_ROOT, hist_cnvtim_save_to)

        # Create output_images folder if it DNE
        hist_path = get_filename(hist_save_to_abs)[0]
        eqim_path = get_filename(eqim_save_to_abs)[0]
        hist_eqim_path = get_filename(hist_eqim_save_to_abs)[0]
        cnvtim_path = get_filename(cnvtim_save_to_abs)[0]
        hist_cnvtim_path = get_filename(hist_cnvtim_save_to_abs)[0]

        if not os.path.isdir(hist_path):
            os.makedirs(hist_path)

        if not os.path.isdir(eqim_path):
            os.makedirs(eqim_path)

        if not os.path.isdir(hist_eqim_path):
            os.makedirs(hist_eqim_path)

        if not os.path.isdir(cnvtim_path):
            os.makedirs(cnvtim_path)

        if not os.path.isdir(hist_cnvtim_path):
            os.makedirs(hist_cnvtim_path)

        generated_hist_path = uimage_path.replace('input_images', 'output_images')

        generated_hist_fname = generate_filename(uimage_fname, 'histogram_')
        generated_eqim_fname = generate_filename(uimage_fname, 'eqim_')
        generated_cnvtim_fname = generate_filename(uimage_fname, 'convert_im_')
        generated_hist_eqim_fname = generate_filename(uimage_fname, 'histogram_eqim_')
        generated_hist_cnvtim_fname = generate_filename(uimage_fname, 'histogram_cnvtim_')

        generated_hist_url = os.path.join(generated_hist_path, generated_hist_fname)
        generated_eqim_url = os.path.join(generated_hist_path, generated_eqim_fname)
        generated_hist_eqim_url = os.path.join(generated_hist_path, generated_hist_eqim_fname)
        generated_cnvtim_url = os.path.join(generated_hist_path, generated_cnvtim_fname)
        generated_hist_cnvtim_url = os.path.join(generated_hist_path, generated_hist_cnvtim_fname)

        histogram_type = request.POST.get('histogram_type')

        Histogram(uploaded_image_url, hist_save_to_abs).do_hist_eq(histogram_type, cnvtim_save_to_abs, hist_cnvtim_save_to_abs, eqim_save_to_abs, hist_eqim_save_to_abs)

        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url,
            'generated_hist_url': generated_hist_url,
            'generated_eqim_url': generated_eqim_url,
            'generated_hist_eqim_url': generated_hist_eqim_url,
            'generated_cnvtim_url': generated_cnvtim_url,
            'generated_hist_cnvtim_url': generated_hist_cnvtim_url
        })

    return render(request, template_name)