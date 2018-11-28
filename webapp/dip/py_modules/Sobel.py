import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
from time import time

from django.conf import settings

class Sobel(object):
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

    def generate_sobel_filtered_image(self, ksize):

        figure = plt.figure()
        figure.add_subplot(1,1,1)
        set_dpi = figure.get_dpi()
        filtered_im = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        start = time()

        if ksize == 90:
            filtered_im = cv2.Sobel(filtered_im,cv2.CV_64F,1,0,ksize=3)  # x

        elif ksize == 0:
            filtered_im = cv2.Sobel(filtered_im,cv2.CV_64F,0,1,ksize=3)  # y

        elif ksize == -45:
            kernel_neg_45 = np.array([[0, 1, 2],
                            [-1,  0, 1],
                            [-2,  -1,  0]])
            filtered_im = cv2.filter2D(filtered_im, cv2.CV_8U, kernel_neg_45)

        elif ksize == 45:
            kernel_plus_45 = np.array([[-2, -1, 0],
                                    [-1,  0, 1],
                                    [0,  1,  2]])
            filtered_im = cv2.filter2D(filtered_im, cv2.CV_8U, kernel_plus_45)

        elif ksize == 999:
            sobelx = cv2.Sobel(filtered_im,cv2.CV_64F,1,0,ksize=3)  # x
            sobely = cv2.Sobel(filtered_im,cv2.CV_64F,0,1,ksize=3)  # y
            filtered_im = cv2.magnitude(sobelx, sobely)

        elif ksize == -999:
            sobelx = cv2.Sobel(filtered_im,cv2.CV_64F,1,0,ksize=3)  # x
            sobely = cv2.Sobel(filtered_im,cv2.CV_64F,0,1,ksize=3)  # y
            filtered_im = cv2.phase(sobelx, sobely)

        end = time()

        ptime = end-start

        figure.set_size_inches(self.image.shape[1]/set_dpi, self.image.shape[0]/set_dpi)
        disp_fig = plt.imshow(filtered_im, cmap = 'gray')
        plt.axis('off')
        disp_fig.axes.get_xaxis().set_visible(False)
        disp_fig.axes.get_yaxis().set_visible(False)

        plt.savefig(self.plotpath, bbox_inches='tight', pad_inches=0, dpi=set_dpi * 1.3)

        return round(ptime,6)