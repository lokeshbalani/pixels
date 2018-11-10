from datetime import date
import os

from django.conf import settings

def images_dirpath(suffix, filename, prefix=None):
    PATH_SUFFIX = suffix

    today = date.today()
    today_path = today.strftime("%Y/%m/%d")

    fname = generate_filename(filename, prefix)
    filepath = os.path.join(PATH_SUFFIX, today_path, fname)

    return filepath

def get_filename(filepath):
    return os.path.split(filepath)

def generate_filename(fname, prefix=None):
    if prefix is not None:
        PATH_PREFIX = prefix 
    else:
        PATH_PREFIX = ''

    return PATH_PREFIX + fname

def clean_media_root():
    physical_files = set()

    # Get all files from the MEDIA_ROOT, recursively
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root is not None:
        for relative_root, dirs, files in os.walk(media_root):
            for file_ in files:
                # Compute the relative file path to the media directory, so it can be compared to the values from the db
                relative_file = os.path.join(os.path.relpath(relative_root, media_root), file_)
                physical_files.add(relative_file)

    # Compute the difference and delete those files
    deletables = physical_files        
    if deletables:
        for file_ in deletables:
            os.remove(os.path.join(media_root, file_))

        # Bottom-up - delete all empty folders
        for relative_root, dirs, files in os.walk(media_root, topdown=False):
            for dir_ in dirs:
                if not os.listdir(os.path.join(relative_root, dir_)):
                    os.rmdir(os.path.join(relative_root, dir_))