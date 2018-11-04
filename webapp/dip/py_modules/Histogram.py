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

    def generate_grayscale_histogram(self, img=None):
        if img is None :
            grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            grayscale_image = img
        
        self.draw_image_histogram(grayscale_image, [0])

    def generate_color_histogram(self, img=None):
        if img is None :
            for i,col in enumerate(self.color):
                self.draw_image_histogram(self.image, [i], col)
        else:
            for i,col in enumerate(self.color):
                self.draw_image_histogram(img, [i], col)
        

    def generate_histogram(self, hist_type='grayscale'):
        figure = plt.figure()
        figure.add_subplot(111)
        
        if hist_type == 'color':
            self.generate_color_histogram()
        else:
            self.generate_grayscale_histogram()

    def save_image(self, img, path, cmap=None):
        figure = plt.figure()
        figure.add_subplot(1,1,1)
        set_dpi = figure.get_dpi()

        figure.set_size_inches(img.shape[1]/set_dpi, img.shape[0]/set_dpi)

        if cmap is None:
            disp_fig = plt.imshow(img)
        else:
            disp_fig = plt.imshow(img, cmap=cmap)
        
        plt.axis('off')
        disp_fig.axes.get_xaxis().set_visible(False)
        disp_fig.axes.get_yaxis().set_visible(False)

        plt.savefig(path, bbox_inches='tight', pad_inches=0, dpi=set_dpi * 1.3)

    def grayscale_equalised(self, im_path, im_hist_path, eq_path, eq_hist_path):
        figure = plt.figure()
        figure.add_subplot(111)
        self.generate_grayscale_histogram()

        grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.save_image(grayscale_image, im_path, 'gray')

        self.plotpath = im_hist_path
        figure = plt.figure()
        figure.add_subplot(111)
        self.generate_grayscale_histogram(grayscale_image)

        eq_grayscale_image = cv2.equalizeHist(grayscale_image)
        self.save_image(eq_grayscale_image, eq_path, 'gray')

        self.plotpath = eq_hist_path
        figure = plt.figure()
        figure.add_subplot(111)
        self.generate_grayscale_histogram(eq_grayscale_image)

    def rgb_equalised(self, im_path, im_hist_path, eq_path, eq_hist_path):
        figure = plt.figure()
        figure.add_subplot(111)
        self.generate_color_histogram()

        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.save_image(rgb_image, im_path)

        figure = plt.figure()
        figure.add_subplot(111)
        self.plotpath = im_hist_path
        self.generate_color_histogram(rgb_image)

        channels = cv2.split(self.image)
        eq_channels = []

        for ch, color in zip(channels, ['B', 'G', 'R']):
            eq_channels.append(cv2.equalizeHist(ch))

        eq_image = cv2.merge(eq_channels)
        eq_image = cv2.cvtColor(eq_image, cv2.COLOR_BGR2RGB)

        self.save_image(eq_image, eq_path)

        self.image = eq_image
        self.plotpath = eq_hist_path
        figure = plt.figure()
        figure.add_subplot(111)
        self.generate_color_histogram(eq_image) 

    def hsv_equalised(self, im_path, im_hist_path, eq_path, eq_hist_path):
        figure = plt.figure()
        figure.add_subplot(111)
        self.generate_color_histogram()

        H, S, V = cv2.split(cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV))
        rgb_image = cv2.cvtColor(cv2.merge([H, S, V]), cv2.COLOR_HSV2RGB)
        self.save_image(rgb_image, im_path)

        figure = plt.figure()
        figure.add_subplot(111)
        self.image = rgb_image
        self.plotpath = im_hist_path
        self.generate_color_histogram(rgb_image)

        eq_V = cv2.equalizeHist(V)
        eq_image = cv2.cvtColor(cv2.merge([H, S, eq_V]), cv2.COLOR_HSV2RGB)

        self.save_image(eq_image, eq_path)

        self.image = eq_image
        self.plotpath = eq_hist_path
        figure = plt.figure()
        figure.add_subplot(111)
        self.generate_color_histogram(eq_image)

    def do_hist_eq(self, hist_type, im_path, im_hist_path, eq_path, eq_hist_path):
        figure = plt.figure()
        figure.add_subplot(111)
        
        if hist_type == 'rgb':
            self.rgb_equalised(im_path, im_hist_path, eq_path, eq_hist_path)
        elif hist_type == 'hsv':
            self.hsv_equalised(im_path, im_hist_path, eq_path, eq_hist_path)
        else:
            self.grayscale_equalised(im_path, im_hist_path, eq_path, eq_hist_path)



