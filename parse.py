import xml.etree.ElementTree as ET
import cv2
import os
import shutil
import argparse

parse = argparse.ArgumentParser(description='the argument used to parse label')
parse.add_argument('--path', '-p', type=str, default='F:/PycharmProjects/LingZhiProj', help='root path')
parse.add_argument('--lb_path', '-l', type=str, default='F:/PycharmProjects/LingZhiProj/Annotations', help='label path')
parse.add_argument('st_path', '-s', type=str, default='F:/PycharmProjects/LingZhiProj/good_labels', help='store path')
parse.add_argument('im_path', '-i', type=str, default='F:/PycharmProjects/LingZhiProj/JPEGImages', help='image path')
args = parse.parse_args()

label_dir = args.lb_path
img_dir = args.im_path
good_label_dir = args.st_path
if os.path.isdir(good_label_dir):
    os.mkdir(good_label_dir)
filelist = {}
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
for _, _, file in os.walk(label_dir):

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
    filelist[filename] = objdict
    imname = os.path.join(img_dir, filename)
    image = cv2.imread(imname)
    for i in range(len(objdict)//5):
        xmin = objdict[i * 5 + 1]
        ymin = objdict[i * 5 + 2]
        xmax = objdict[i * 5 + 3]
        ymax = objdict[i * 5 + 4]
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        cv2.putText(image, objdict[i * 5], (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 6, (0, 0, 255), 2)
    cv2.imshow('image', image)
    keyout = cv2.waitKey(0)
    if keyout==121:
        print('label for {} is qualified, it will be move to the label dir'.format(file))
        shutil.move(file, good_label_dir)
    elif keyout==110:
        print('label for {} is uncertain, it will remain at current location'.format(file))
    else:
        raise ValueError('unrecognizing input!!!')
    print(objdict)

