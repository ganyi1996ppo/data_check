import xml.etree.ElementTree as ET
import cv2
import os
import shutil
import argparse


parse = argparse.ArgumentParser(description='the argument used to parse label')
parse.add_argument('--path', '-p', type=str, default='/home/ganyi/darknet/wajueji', help='root path')
parse.add_argument('--lb_path', '-l', type=str, default='/home/ganyi/darknet/wajueji/wehave_label', help='label path')
parse.add_argument('--st_path', '-s', type=str, default='/home/ganyi/darknet/wajueji/wehave_good_labels', help='store path')
parse.add_argument('--fi_path', '-f', type=str, default='/home/ganyi/darknet/wajueji/wehave_bad_labels', help='bad label')
parse.add_argument('--im_path', '-i', type=str, default='/data1/datasets/wajueji/images', help='image path')
args = parse.parse_args()

label_dir = args.lb_path
img_dir = args.im_path
good_label_dir = args.st_path
bad_label_dir = args.fi_path
if not os.path.isdir(good_label_dir):
    os.mkdir(good_label_dir)
if not os.path.isdir(bad_label_dir):
    os.mkdir(bad_label_dir)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
review_flag = False
filelist = []
class Label_iter(object):
    def __init__(self,
                 label_dir,
                 class_list):
        self.label_dir = label_dir
        self.class_list = class_list

    for _, _, files in os.walk(label_dir):
        for file in files:
            if review_flag == True:
                file = filelist[-1]
                filelist.pop(-1)
                review_flag=False
            filepath = os.path.join(label_dir, file)
            print(filepath)
            tree = ET.parse(filepath)
            root = tree.getroot()
            obj = root.findall('object')
            filename = root.find('filename').text
            objdict = []
            for ob in obj:
                objdict.append(ob.find('name').text)
                bndbox = ob.find('bndbox')
                objdict.append(int(bndbox.find('xmin').text))
                objdict.append(int(bndbox.find('ymin').text))
                objdict.append(int(bndbox.find('xmax').text))
                objdict.append(int(bndbox.find('ymax').text))
        imname = os.path.join(img_dir, filename)
        if not os.path.isfile(imname):
            continue
        image = cv2.imread(imname)
        if not os.path.isfile(image):
            continue
        for i in range(len(objdict)//5):
            xmin = objdict[i * 5 + 1]
            ymin = objdict[i * 5 + 2]
            xmax = objdict[i * 5 + 3]
            ymax = objdict[i * 5 + 4]
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            cv2.putText(image, objdict[i * 5], (xmax, ymax), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        cv2.imshow('image', image)
        # This list will store 10 images for you to undo your choice
        keyout = cv2.waitKey(0)
        if keyout==121:
            print('label for {} is qualified, it will be move to the good label dir'.format(file))
            fpath = os.path.join(good_label_dir, file)
            filelist.append(fpath)
            if not os.path.isfile(fpath):
                shutil.move(os.path.join(label_dir, file), good_label_dir)
        elif keyout==110:
            print('label for {} is uncertain, it will be move to the bad label dir'.format(file))
            fpath = os.path.join(bad_label_dir, file)
            filelist.append(fpath)
            if not os.path.isfile(fpath):
                shutil.move(os.path.join(label_dir, file), bad_label_dir)
        elif keyout==98:
            print('look at the previous label')
            review_flag = True
        else:
            raise ValueError('unrecognizing input!!!')
        print(objdict)

