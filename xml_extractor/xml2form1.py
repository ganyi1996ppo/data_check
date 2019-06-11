#!/usr/bin/env python
import xml.etree.ElementTree as ET
import os
import collections

s = os.sep
labelfile = '/data1/datasets/VOC/'
testfile = os.path.join(labelfile, '2007_test.txt')
trainfile = os.path.join(labelfile, '2007_train.txt')
valfile = os.path.join(labelfile, '2007_val.txt')
filelist = [testfile, trainfile, valfile]
for i, file in enumerate(filelist):
    with open(file) as f:
        data = open(str(i)+'xml.txt', 'w')
        alldata = f.readlines()
        for line in alldata:
            imagedir = line.strip()
            imagename = os.path.basename(imagedir)[:-3]
            dir = os.path.dirname(os.path.dirname(imagedir))
            Annotation = os.path.join(dir, 'Annotations', imagename+'xml')
            tree = ET.parse(Annotation)
            root = tree.getroot()
            filename = os.path.join('/data1/datatsets/VOC/VOCdevkit/VOC2007/JPEGImages', root.find('filename'))
            allobj = root.findall('object')
            for obj in allobj:
                if obj.find('name').text == 'person':
                    bndbox = obj.find('bndbox')
                    xmin = bndbox.find('xmin').text
                    ymin = bndbox.find('ymin').text
                    xmax = bndbox.find('xmax').text
                    ymax = bndbox.find('ymax').text
                    print(filename,',',xmin,',',ymin,',',xmax,',',ymax,',',0,file=data)
        data.close()


