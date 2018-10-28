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

    def generate_histogram(self):
        ch = self.get_nchannels()

        figure = plt.figure()
        figure.add_subplot(111)

        if ch > 1:
            for i,col in enumerate(self.color):
                histr = cv2.calcHist([self.image],[i],None,[256],[0,256])
                plt.plot(histr,color = col)
                plt.xlim([-10,266])
        else:
            histr = cv2.calcHist([self.image],[0],None,[256],[0,256])
            plt.plot(histr,color = 'gray')
            plt.xlim([-10,266])
        
        plt.savefig(self.plotpath)


