from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os

from .helpers import get_filename, images_dirpath, generate_filename, clean_media_root

def connected_components_view(request):
    clean_media_root()

    template_name = 'modules/morphological/connected-components.html'
    return render(request, template_name)