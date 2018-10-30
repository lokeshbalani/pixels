from datetime import date
import os

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