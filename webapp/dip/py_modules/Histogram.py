import numpy as np
import cv2

class Histogram(object):
    def __init__(self, impath):
        self.impath = impath
        print(impath)
        print(self.impath)
        self.image = cv2.imread(self.impath)
        self.channel = ('b','g','r')

    def get_image(self):
        return self.image

    def get_nchannels(self):
        if self.image.shape[2] > 1:
            ch = self.image.shape[2]
        else:
            ch = 1

        return ch

    def generate_histogram(self):
        ch = self.get_nchannels()
        histr = np.zeros((ch, 256), np.int32)

        for i,channel in enumerate(ch):
            histr[i] = cv2.calcHist([self.image],[i],None,[256],[0,256])

        return histr
