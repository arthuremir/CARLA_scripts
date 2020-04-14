import carla

from config import *


class Vehicle:
    pass


class Camera:

    def __init__(self, bp, sensor_type):

        self.bp = bp
        self.sensor_type = sensor_type
        self.cam = None

        if sensor_type == 'rgb':
            self.cam = self.bp.find('sensor.camera.rgb')
        elif sensor_type == 'depth':
            self.cam = self.bp.find('sensor.camera.depth')

        self.cam.set_attribute('image_size_x', f'{IMG_WIDTH}')
        self.cam.set_attribute('image_size_y', f'{IMG_HEIGHT}')
        self.cam.set_attribute('fov', '110')

    def get_type(self):
        return self.sensor_type
