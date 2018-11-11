import cv2
from matplotlib import pyplot as plt

import os
from django.conf import settings

class Bilateral(object):
    def __init__(self, impath, pltpath):
        self.impath = self.get_path(impath)
        self.image = cv2.imread(self.impath)
        #self.color = ('b','g','r')
        self.plotpath = pltpath

    def get_image(self):
        return self.image

    def get_path(self, impath):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        MEDIA_ROOT_DIR = ROOT_DIR.replace('/dip/py_modules', '')
        abs_impath = MEDIA_ROOT_DIR + impath

        return abs_impath

    def generate_bilateral_filtered_image(self, ksize, sigmaColor = 30, sigmaSpace = 30):

        figure = plt.figure()
        figure.add_subplot(1,1,1)
        set_dpi = figure.get_dpi()

        bilateral_im = cv2.bilateralFilter(self.image, ksize, sigmaColor, sigmaSpace)
        bilateral_im = cv2.cvtColor(bilateral_im, cv2.COLOR_BGR2RGB)

        figure.set_size_inches(self.image.shape[1]/set_dpi, self.image.shape[0]/set_dpi)
        disp_fig = plt.imshow(bilateral_im)
        plt.axis('off')
        disp_fig.axes.get_xaxis().set_visible(False)
        disp_fig.axes.get_yaxis().set_visible(False)

        plt.savefig(self.plotpath, bbox_inches='tight', pad_inches=0, dpi=set_dpi * 1.3)