import pygame
from pygame import Vector2


class Hand:
    """
    Represents information on a detected hand.
    """
    def __init__(self, landmarks: list[tuple[int, int]], gesture: str):
        """
        Initializes the `Hand` object.
        :param landmarks: Landmarks (21) of the hand.
        :param gesture: Detected gesture.
        """
        self.landmarks = landmarks
        self.gesture = gesture

    def bounding_box(self) -> pygame.Rect:
        """
        Retrieves a bounding box as `Rect` of the Hand.
        :return: A rect containing all landmarks of the hand.
        """
        x, y = zip(*self.landmarks)
        x1, y1, x2, y2 = min(x), min(y), max(x), max(y)
        return pygame.Rect(x1, y1, x2-x1, y2-y1)
