import numpy as np
from matplotlib import pyplot as plt

from mxnet import nd, gpu

from gluoncv import model_zoo, data, utils
from bounding_box import bounding_box as bb

from config import *

MODEL_NAME = 'ssd_512_resnet50_v1_voc'

INPUT_W = IMG_WIDTH // 2
INPUT_H = IMG_HEIGHT // 2


class Detector:
    def __init__(self):
        self.net = model_zoo.get_model(MODEL_NAME, pretrained=True)

    def predict(self, raw_image):
        x, img = data.transforms.presets.ssd.transform_test(nd.array(raw_image), short=INPUT_H)
        print('Shape of pre-processed image:', x.shape)

        class_IDs, scores, bounding_boxes = self.net(x)
        print(bounding_boxes[0][0])
        for box in bounding_boxes:
        #    print(box)
            #    print(box)
            bb.add(img, box[0][0], box[0][3], box[0][1], box[0][2], "a", (255, 255, 255))
        # print(bounding_boxes.shape)

        # ax = utils.viz.plot_bbox(x, bounding_boxes[0], scores[0],
        #                         class_IDs[0], class_names=self.net.classes)
        # plt.show()

        return [class_IDs, scores, bounding_boxes]
