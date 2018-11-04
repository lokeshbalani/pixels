import numpy as np
import cv2
from matplotlib import pyplot as plt

import os
from django.conf import settings

class Histogram(object):
    def __init__(self, impath, pltpath):
        self.impath = self.get_path(impath)
        self.image = cv2.imread(self.impath)
        self.color = ('b','g','r')
        self.plotpath = pltpath

    def get_image(self):
        return self.image

    def get_path(self, impath):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        MEDIA_ROOT_DIR = ROOT_DIR.replace('/dip/py_modules', '')
        abs_impath = MEDIA_ROOT_DIR + impath

        return abs_impath

    def get_nchannels(self):
        if self.image.shape[2] > 1:
            ch = self.image.shape[2]
        else:
            ch = 1

        return ch

    def draw_image_histogram(self, img, channel, color='k'):
        hist = cv2.calcHist([img], channel, None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256]) 
        plt.savefig(self.plotpath, bbox_inches='tight', pad_inches=0)

    def generate_grayscale_histogram(self):
        grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.draw_image_histogram(grayscale_image, [0])

    def generate_color_histogram(self):
        for i,col in enumerate(self.color):
            self.draw_image_histogram(self.image, [i], col)

    def generate_histogram(self, hist_type='grayscale'):
        figure = plt.figure()
        figure.add_subplot(111)
        
        if hist_type == 'color':
            self.generate_color_histogram()
        else:
            self.generate_grayscale_histogram()


