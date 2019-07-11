import xml.etree.ElementTree as ET
import os
from label_iter_base import Label_Iter_Base

class XML2DarkNet(Label_Iter_Base):
    def __init__(self,
                 dest_dir='/home/ganyi/darknet/wajueji/new_labels',
                 **kwargs):
        super(XML2DarkNet, self).__init__(**kwargs)
        self.dest_dir = dest_dir
        self.class_dict = {name:index for index, name
                           in enumerate(self.class_names)}

    def convert_bbox(self, size, box):
        dw = 1./(size[1])
        dh = 1./(size[0])
        x = (box[0] + box[2])/2.0 - 1
        y = (box[1] + box[3])/2.0 - 1
        w = box[2] - box[0]
        h = box[3] - box[1]
        x = x * dw
        y = y * dh
        w = w * dw
        h = h * dh
        return (x,y,w,h)

    def execute_information(self, im_info, label_info):
        obj_num = len(label_info)//5
        im_name, height, width = im_info
        dest_file = open(os.path.join(self.dest_dir, im_name[:-3]+'txt'), 'w')
        for obj in range(obj_num):
            class_id = self.class_dict[label_info[obj*5]]
            bbox = label_info[obj*5+1:obj*5+5]
            bb = self.convert_bbox((height, width), bbox)
            dest_file.write(str(class_id) + ' ' + ' '.join([str(a) for a in bb]) + '\n')
        dest_file.close()

    def generate_txt(self):
        train_txt = open(os.path.join(self.dest_dir, 'train.txt'), 'w')
        test_txt = open(os.path.join(self.dest_dir, 'test.txt'), 'w')
        for _,_,files in os.walk(self.dest_dir):
            for i, file in enumerate(files):
                if i%10 == 0:
                    test_txt.write(os.path.join(self.img_dir, file[:-3]+'jpg')+'\n')
                else:
                    train_txt.write(os.path.join(self.img_dir, file[:-3]+'jpg')+'\n')
        train_txt.close()
        test_txt.close()


if __name__ == '__main__':
    model = XML2DarkNet()
    #model.Iter_labels()
    model.generate_txt()
    print('Done!')











