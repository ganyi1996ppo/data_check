import xml.etree.ElementTree as ET
import os
from label_iter_base import Label_Iter_Base

class XML2DarkNet(Label_Iter_Base):
    def __init__(self,
                 dest_dir,
                 **kwargs):
        super(XML2DarkNet, self).__init__(**kwargs)
        self.dest_dir = dest_dir
        self.class_dict = {name:index for name, index
                           in enumerate(self.class_names)}

    def convert_bbox(self, size, box):
        dw = 1./(size[1])
        dh = 1./(size[0])
        x = (box[0] + box[2])/2.0 - 1
        y = (box[1] + box[3])/2.0 - 1
        w = box[0] - box[2]
        h = box[1] - box[3]
        x = x * dw
        y = y * dh
        w = w * dw
        h = h * dh
        return (x,y,w,h)

    def execute_information(self, im_info, label_info):
        obj_num = len(label_info)//5
        im_name, height, width = im_info
        dest_file = open(os.path.join(self.dest_dir, im_name[:-3]+'txt'))
        for obj in range(obj_num):
            class_id = self.class_dict[label_info[obj*5]]
            bbox = label_info[obj*5+1:obj*5+4]
            bb = self.convert_bbox((height, width), bbox)
            dest_file.write(str(class_id) + ' ' + ' '.join([str(a) for a in bb]) + '\n')











