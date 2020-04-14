import numpy as np

from config import *
from carla import ColorConverter as cc

def to_numpy(frame, type):
    #print(frame.frame_number, type)
    #frame.convert(cc.LogarithmicDepth)
    frame = np.array(frame.raw_data)
    frame = frame.reshape((IMG_HEIGHT, IMG_WIDTH, 4))
    frame = frame[:, :, :3]
    frame = frame[:, :, ::-1]
    frame = frame.swapaxes(0, 1)

    return frame
