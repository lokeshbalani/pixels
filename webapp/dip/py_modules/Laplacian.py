import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
from time import time

from django.conf import settings

class Laplacian(object):
    def __init__(self, impath, pltpath):
        self.impath = self.get_path(impath)
        self.image = cv2.imread(self.impath)
        #self.color = ('b','g','r')
        self.plotpath = pltpath
        self.dim = self.image.shape

    def get_image(self):
        return self.image

    def get_im_dim(self):
        return self.dim

    def get_path(self, impath):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        MEDIA_ROOT_DIR = ROOT_DIR.replace('/dip/py_modules', '')
        abs_impath = MEDIA_ROOT_DIR + impath

        return abs_impath

    def generate_laplacian_filtered_image(self, ksize, sigma=1):

        figure = plt.figure()
        figure.add_subplot(1,1,1)
        set_dpi = figure.get_dpi()
        filtered_im = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        start = time()

        if ksize == 0:
            pass

        elif ksize == 90:
            filtered_im = cv2.GaussianBlur(filtered_im, (3, 3), 1)

        elif ksize == -45:
            filtered_im = cv2.GaussianBlur(filtered_im, (7, 7), 1)

        elif ksize == 450:
            filtered_im = cv2.GaussianBlur(filtered_im, (7, 7), 2)

        elif ksize == 999:
            filtered_im = cv2.GaussianBlur(filtered_im, (13, 13), 2)

        elif ksize == -999:
            filtered_im = cv2.GaussianBlur(filtered_im, (21, 21), 3)

        else:
            filtered_im = cv2.GaussianBlur(filtered_im, (ksize, ksize), 1)


        filtered_im = cv2.Laplacian(filtered_im,cv2.CV_64F)

        end = time()

        ptime = end-start

        figure.set_size_inches(self.image.shape[1]/set_dpi, self.image.shape[0]/set_dpi)
        disp_fig = plt.imshow(filtered_im, cmap = 'gray')
        plt.axis('off')
        disp_fig.axes.get_xaxis().set_visible(False)
        disp_fig.axes.get_yaxis().set_visible(False)

        plt.savefig(self.plotpath, bbox_inches='tight', pad_inches=0, dpi=set_dpi * 1.3)

        return round(ptime,6)