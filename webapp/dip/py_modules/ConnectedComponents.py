import cv2
from matplotlib import pyplot as plt
import os
from time import time
import numpy as np

from django.conf import settings

class ConnectedComponents(object):
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

    def generate_cc_label_image(self, connectivity):

        figure = plt.figure()
        figure.add_subplot(1,1,1)
        set_dpi = figure.get_dpi()

        start = time()
        b_im = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)[1]
        ret, labels = cv2.connectedComponents(b_im[:,:,0], connectivity=connectivity)
        end = time()

        ptime = end-start

        # Map component labels to hue val
        label_hue = np.uint8(179*labels/np.max(labels))
        blank_ch = 255*np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

        # cvt to BGR for display
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

        # set bg label to black
        labeled_img[label_hue==0] = 0

        figure.set_size_inches(self.image.shape[1]/set_dpi, self.image.shape[0]/set_dpi)
        disp_fig = plt.imshow(labeled_img, cmap = 'gray')
        plt.axis('off')
        disp_fig.axes.get_xaxis().set_visible(False)
        disp_fig.axes.get_yaxis().set_visible(False)

        plt.savefig(self.plotpath, bbox_inches='tight', pad_inches=0, dpi=set_dpi * 1.3)

        return round(ptime,6)