import random
import time
import threading

import pygame
import numpy as np
import cv2

import carla

from config import *
from utils import *
from actors import *
from models.gl import Detector


class Env:
    SHOW_CAM = True
    STEER_AMT = 1.0

    im_width = IMG_WIDTH
    im_height = IMG_HEIGHT
    actor_list = []

    front_camera = None
    collision_hist = []

    def __init__(self):
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(2.0)

        self.world = self.client.get_world()

        spawn_points = self.world.get_map().get_spawn_points()

        self.transform = spawn_points[1]
        self.cam_transform = carla.Transform(carla.Location(x=2.5, z=0.7))

        self.blueprint_library = self.world.get_blueprint_library()

        self.vehicle_list = []
        self.camera_list = []

        self.detector = Detector()

    def reset(self):

        model_3 = self.blueprint_library.filter('model3')[0]
        self.vehicle = self.world.spawn_actor(model_3, self.transform)
        self.vehicle_list.append(self.vehicle)

        self.rgb_cam = Camera(self.blueprint_library, 'rgb')
        self.camera_list.append(self.rgb_cam)

        # self.depth_cam = Camera(self.blueprint_library, 'depth')
        # self.camera_list.append(self.depth_cam)

        self.display = pygame.display.set_mode(
            (IMG_WIDTH * len(self.camera_list), IMG_HEIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        for i, cam in enumerate(self.camera_list):
            self.camera_list[i] = self.world.spawn_actor(cam.cam, self.cam_transform, attach_to=self.vehicle)
            self.camera_list[i].listen(lambda data: self.process_sensor_data(data, cam.get_type()))

        # self.vehicle.apply_control(carla.VehicleControl(brake=0.0, throttle=1.0))

    def destroy_actors(self):
        for actor in self.vehicle_list:
            actor.destroy()
        for actor in self.camera_list:
            actor.destroy()

    def process_sensor_data(self, frame, type):

        img = to_numpy(frame, type)
        #print(img.shape)
        if img.shape == (640, 480, 3):
            x = threading.Thread(target=self.detector.predict, args=(img, ))
            x.start()

            #ret = self.detector.predict(img)
        # print(ret)

        if self.SHOW_CAM:
            picture = pygame.surfarray.make_surface(img)
            self.display.blit(picture, (0, 0))
            pygame.display.flip()
            pygame.event.pump()


# torch 1.3.1
# gcc 9.2.1
# nv 440

'''
#include <ATen/ATen.h>
#include <ATen/cuda/CUDAContext.h>

#include <THC/THC.h>
#include <THC/THCAtomics.cuh>
#include <THC/THCDeviceUtils.cuh>
'''
