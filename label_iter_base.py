import xml.etree.ElementTree as ET
import os
import cv2
import re
import collections


class Label_Iter_Base(object):
    def __init__(self,
                 label_dir,
                 img_dir,
                 class_names,
                 iter_mode='generator'):
        assert iter_mode=='generator', 'iter mode only support generator now, list mode will be updated soon'
        self.iter_mode = iter_mode
        self.label_dir = label_dir
        self.img_dir = img_dir
        self.class_names = class_names

    def XML_extractor(self, dirname):
        information = []
        tree = ET.parse(dirname)
        root = tree.getroot()
        obj = root.findall('object')
        re_imname = root.find('filename').text
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        im_information = (re_imname,height, width)
        for ob in obj:
            information.append(ob.find('name').text)
            bndbox = ob.find('bndbox')
            information.append(int(bndbox.find('xmin').text))
            information.append(int(bndbox.find('ymin').text))
            information.append(int(bndbox.find('xmax').text))
            information.append(int(bndbox.find('ymax').text))
        return im_information, information

    def Iter_labels(self):
        if self.iter_mode == 'generator':
            for _,_,files in os.walk(self.label_dir):
                for file in files:
                    im_information, label_information = self.XML_extractor(file)
                    self.execute_information(im_information, label_information)

    def execute_information(self, im_info, label_info):
        raise NotImplementedError


