import cv2
from matplotlib import pyplot as plt

import os
from django.conf import settings

class Median(object):
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

    def generate_median_filtered_image(self):

        figure = plt.figure()
        figure.add_subplot(111)

        median_im = cv2.medianBlur(self.image, 3)
        plt.imshow(median_im,cmap = 'gray')
        plt.savefig(self.plotpath)