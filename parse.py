import xml.etree.ElementTree as ET
import cv2
import os
label_dir = os.path.join(os.getcwd(),'Annotation')
img_dir = os.path.join(os.getcwd(),'JPEGImge')
filelist = {}
for file in os.listdir(label_dir):

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
    print(objdict)
for filename in filelist.keys():
    objlist = filelist[filename]
    filename = os.path.join(img_dir, filename)
    image = cv2.imread(filename)
    for i in range(len(objlist)//5):
        xmin = objlist[i*5+1]
        ymin = objlist[i*5+2]
        xmax = objlist[i*5+3]
        ymax = objlist[i*5+4]
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        cv2.putText(image, objlist[i*5], (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX,6, (0,0,255),10)
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.imshow('image', image)
    cv2.waitKey(0)