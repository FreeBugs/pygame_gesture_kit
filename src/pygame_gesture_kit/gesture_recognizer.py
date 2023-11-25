import copy
from importlib.resources import files
import threading
import time
from pathlib import Path

import mediapipe as mp
from mediapipe.tasks import python
import pygame.display
from mediapipe.tasks.python.vision import GestureRecognizerResult
from .hand import Hand


class GestureRecognizer:
    """
    The `GestureRecognizer` is responsible for detecting hands, tracking movements and estimating gestures.
    """

    def __init__(self, capture_device, max_hands=2, min_detection_confidence=.7, min_tracking_confidence=.7,
                 custom_model_path=None):
        """
        Initializes a GestureRecognizer with the capture device (camera) specified. The parameters for hand recognition
        settings are passed to MediaPipe.
        :param capture_device: The `Camera` to use for capturing images.
        :param max_hands: The maximum number of hands to detect (passed to MediaPipe).
        :param min_detection_confidence: The minimum detection confidence (passed to MediaPipe).
        :param min_tracking_confidence: The minimum confidence to consider tracking between frames
        (passed to MediaPipe).
        :param custom_model_path: A custom model can be loaded by the recognizer.
        """
        self._visible_hands = 0
        self._capture_device = capture_device
        self._is_running = False
        self._worker = None
        self._hands = []
        self._timestamp = 0
        self._screen_width, self.__screen_height = pygame.display.get_surface().get_size()
        self._mutex = threading.Lock()

        model_path = custom_model_path
        if model_path is None:
            model_path = Path(str(files('pygame_gesture_kit')))
            model_path = model_path.joinpath(Path('model')).joinpath(Path('hagrid.task'))
        if not model_path.exists():
            raise FileNotFoundError(model_path)

        base_options = mp.tasks.BaseOptions
        gesture_recognizer = mp.tasks.vision.GestureRecognizer
        gesture_recognizer_options = mp.tasks.vision.GestureRecognizerOptions
        vision_running_mode = mp.tasks.vision.RunningMode
        options = gesture_recognizer_options(
            base_options=base_options(
                model_asset_path=model_path),
            num_hands=max_hands,
            min_tracking_confidence=min_tracking_confidence,
            min_hand_detection_confidence=min_detection_confidence,
            running_mode=vision_running_mode.LIVE_STREAM,
            result_callback=self._recognizer_callback)

        self.gesture_recognizer = gesture_recognizer.create_from_options(options)

    def _mp_to_pygame_coords(self, c):
        if self._capture_device.mirror:
            x = c.x * self._screen_width
            y = c.y * self.__screen_height
        else:
            x = (1 - c.x) * self._screen_width
            y = c.y * self.__screen_height
        return x, y

    def _recognizer_callback(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if result.hand_landmarks:
            hands = []
            gestures = []
            for hand in result.hand_landmarks:
                hands.append([self._mp_to_pygame_coords(c) for c in hand])
            if result.gestures is not None:
                gestures = [ges.category_name for hand in result.gestures for ges in hand]
            with self._mutex:
                self._visible_hands = len(hands)
                self._hands = []
                for i in range(0, len(hands)):
                    self._hands.append(Hand(
                        hands[i],
                        gestures[i] if len(gestures) > i else None
                    ))
        else:
            with self._mutex:
                self._visible_hands = 0
                self._hands = []

    def _gesture_thread_function(self):
        while self._is_running:
            cap = self._capture_device.raw
            if cap is not None:
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cap)
                self._timestamp += 1
                self.gesture_recognizer.recognize_async(mp_image, self._timestamp)
                time.sleep(.01)

    def start(self) -> None:
        """
        Starts capturing images from the `Camera` and processing of tracking and gesture recognition.
        :return:
        """
        self._is_running = True
        self._worker = threading.Thread(target=self._gesture_thread_function)
        self._worker.start()

    def stop(self) -> None:
        """
        Stops capturing and processing images.
        :return:
        """
        self._is_running = False
        self._worker.join()

    def get_hands(self) -> list[Hand]:
        """
        Retrieves the current list of `Hand` objects. All detected hands with their landmarks and gestures are returned
        in the same order as MediaPipe detects them. That is not necessarily from left to right but more in the order
        MediaPipe has started tracking them.
        :return: List of `Hand`.
        """
        with self._mutex:
            return copy.deepcopy(self._hands)

    def get_visible_hands(self) -> int:
        """
        Retrieves the number of visible hands.
        :return: The number of hands as `int` or `0` if none are visible.
        """
        with self._mutex:
            return self._visible_hands
