import cv2
from matplotlib import pyplot as plt
import os
from time import time
import numpy as np

from django.conf import settings

class Closing(object):
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

    def generate_closing_filtered_image(self, ksize):

        figure = plt.figure()
        figure.add_subplot(1,1,1)
        set_dpi = figure.get_dpi()

        filtered_im = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((ksize, ksize), np.uint8)

        start = time()
        filtered_im = cv2.morphologyEx(filtered_im, cv2.MORPH_CLOSE, kernel)
        end = time()

        ptime = end-start

        #filtered_im = cv2.cvtColor(filtered_im, cv2.COLOR_BGR2RGB)

        figure.set_size_inches(self.image.shape[1]/set_dpi, self.image.shape[0]/set_dpi)
        disp_fig = plt.imshow(filtered_im, cmap = 'gray')
        plt.axis('off')
        disp_fig.axes.get_xaxis().set_visible(False)
        disp_fig.axes.get_yaxis().set_visible(False)

        plt.savefig(self.plotpath, bbox_inches='tight', pad_inches=0, dpi=set_dpi * 1.3)

        return round(ptime,6)