import os
from bs4 import BeautifulSoup


class Entity():
    def __init__(self, name, xmin, xmax, ymin, ymax, difficult, truncated):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.difficult = difficult
        self.truncated = truncated


class Data():
    def __init__(self, root_dir, image_name):
        self.image_name = image_name
        self.image_path = os.path.join(root_dir, "images", image_name )
        self.annotation_path = os.path.join(root_dir, "annotations", image_name[:-4] + ".xml")
        self.annotations = self.load_masks()
        #print(self.image_path)
        #print(self.image_name)
        #print(self.annotations)
        #print(self.annotation_path)

    def load_masks(self):
        annotations = []
        xml_content = open(self.annotation_path).read()
        bs = BeautifulSoup(xml_content, 'xml')
        objs = bs.findAll('object')
        for obj in objs:
            obj_name = obj.findChildren('name')[0].text
            difficult = int(obj.findChildren('difficult')[0].contents[0])
            truncated = int(obj.findChildren('truncated')[0].contents[0])
            bbox = obj.findChildren('bndbox')[0]
            xmin = int(bbox.findChildren('xmin')[0].contents[0])
            ymin = int(bbox.findChildren('ymin')[0].contents[0])
            xmax = int(bbox.findChildren('xmax')[0].contents[0])
            ymax = int(bbox.findChildren('ymax')[0].contents[0])
            annotations.append(Entity(obj_name, xmin, xmax, ymin, ymax, difficult, truncated))
        return annotations
