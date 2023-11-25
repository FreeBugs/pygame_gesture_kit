import threading

import cv2
import numpy as np
import pygame


def create_surface_from_frame(frame):
    surface = np.rot90(frame)
    surface = pygame.surfarray.make_surface(surface)
    return surface


class Camera:
    def __init__(self, mirror=False):
        self.cap = None
        self.raw = None
        self.surface = None
        self.worker = None
        self.is_running = False
        self.mirror = mirror

    def read_camera(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def camera_thread_function(self):
        while self.is_running:
            self.raw = self.read_camera()
            if self.mirror:
                self.surface = pygame.transform.flip(create_surface_from_frame(self.raw), True, False)
            else:
                self.surface = create_surface_from_frame(self.raw)

    def open_camera(self, camera_index):
        if not self.cap:
            self.cap = cv2.VideoCapture(camera_index)
            self.is_running = True
            self.worker = threading.Thread(target=self.camera_thread_function)
            self.worker.start()
        else:
            raise RuntimeError('Camera already open.')

    def close_camera(self):
        if self.cap:
            self.is_running = False
            self.worker.join()
            self.cap.release()
            self.cap = None

    def get_surface(self):
        return self.surface
