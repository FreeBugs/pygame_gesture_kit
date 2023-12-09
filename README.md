# pygame_gesture_kit
**Easy camera based hand tracking and gesture recognition for pygame**

Take a look at the [PyGame-ComputerVision-Racer 🚗](https://github.com/FreeBugs/pygame_cv_racer) game for an example
project.

## How it works
pygame_gesture_kit uses [MediaPipe](https://developers.google.com/mediapipe) and  [OpenCV](https://opencv.org/) to
capture a video feed from a camera and detect hands in these images.

The camera frame is mapped to the pygame window and tracking coordinates for all hand landmarks can be acquired by
calling the function `get_hands()` from within the game loop. It also provides information on detected gesture.
Capturing from a camera from within the game loop would limit the frame rate of your game to that of the camera,
which might cause the framerate to drop to 30 fps or even lower. To prevent this, pygame_gesture_kit executes video 
capturing and processing in a separate thread.

The gesture recognition uses a customized model, trained from the [HaGRID dataset](https://arxiv.org/abs/2206.08219).
It provides the following labels:
* `none` if no gesture was detected,
* `fist` for a closed hand,
* one finger: `one`
* two fingers: `two_up`, `two_up_inverted`, `peace`, `peace_inverted`
* three fingers: `three`, `three2`
* four fingers: `four`
* five fingers: `palm`, `stop`, `stop_inverted`
* thumbs up/down: `like`, `dislike`

## How to use it

A comprehensive example is provided in the `example` directory. Basically, you need to import and use two classes
in your code: the `Camera` and `GestureRecognizer`.

```python
from pygame_gesture_kit import GestureRecognizer, Camera
import pygame_gesture_kit.hand_visualizer
```

The `Camera` class wraps an OpenCV capture device and uses the same index numbers to specify devices. Unfortunately,
OpenCV does not provide an interface to enumerate cameras, so you will have to guess, which is the right index for
you. It will usually be `0`, but on macOS that index may also be the continuity camera. Try `1` and higher numbers
if you don't get the camera you want.

You can start capturing and recognizing hands easily like this:

```python
capture_device = Camera()
try:
    capture_device.open_camera(0)
except Exception as e:
    print(e)
    exit(1)
gesture_recognizer = GestureRecognizer(capture_device, max_hands=2)
gesture_recognizer.start()
```

The number of visible hands can be determined by the `gesture_recognizer.get_visible_hands()` function.

The following code snippet illustrates how to process data from the `get_hands()` function. It uses the `hand_visualizer`
to draw the detected landmarks on a surface and adds labels for the detected gestures.
```python
i_hand = 0
for hand in gesture_recognizer.get_hands():
    hand_visualizer.draw_bones(screen, hand, joint_label_font=small_font)
    i_hand += 1
    text = font.render(f'Hand {i_hand}', 1, pygame.Color('black'), pygame.Color('white'))
    x, y = hand.landmarks[0]
    screen.blit(text, (x, y))
    text = font.render(f'Gesture: {hand.gesture}', 1, pygame.Color('black'), pygame.Color('white'))
    screen.blit(text, (x, y + 24))
```

## Installing
You can install pygame_gesture_kit using the PyPI package manager:
```shell
python -m pip install pygame-gesture-kit
```
alternatively, install it directly from this github repo:
```shell
python -m pip install git+https://github.com/FreeBugs/pygame_gesture_kit.git
```

If you are using PyCharm, you can install the package from the Package Manager by selecting
**Add Package** -> **From Version Control**.
