import os
import platform

import pygame

from pygame_gesture_kit import hand_visualizer
from pygame_gesture_kit import GestureRecognizer, Camera


def show_fps(surf, font, clock):
    fps = f'FPS: {clock.get_fps():.2f}'
    rendered_fps = font.render(fps, 1, pygame.Color("blue"))
    x = surf.get_rect().w - font.size(fps)[0]
    surf.blit(rendered_fps, (x, 0))


if __name__ == '__main__':
    preferred_cam = 0
    pygame.init()

    screen_width = 1280
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PygameGestureKit Demo")

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 24, bold=True)
    small_font = pygame.font.SysFont("monospace", 20)

    capture_device = Camera()
    try:
        capture_device.open_camera(preferred_cam)
    except Exception as e:
        print(e)
        exit(1)
    gesture_recognizer = GestureRecognizer(capture_device, max_hands=4)
    gesture_recognizer.start()

    is_running = True
    cam_image = None
    while is_running:
        screen.fill(pygame.Color('white'))

        if capture_device.surface is not None:
            c = pygame.transform.scale(capture_device.surface, (screen_width, screen_height))
            c.set_alpha(128)
            screen.blit(c, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                is_running = False
                break

        show_fps(screen, font, clock)

        num_hands = f'Visible hands: {gesture_recognizer.get_visible_hands()}'
        rendered_num_hands = font.render(num_hands, 1, pygame.Color('white'), pygame.Color('black'))
        screen.blit(rendered_num_hands, (0, 0))

        i_hand = 0
        for hand in gesture_recognizer.get_hands():
            hand_visualizer.draw_bones(screen, hand, joint_label_font=small_font)
            i_hand += 1
            text = font.render(f'Hand {i_hand}', 1, pygame.Color('black'), pygame.Color('white'))
            x, y = hand.landmarks[0]
            screen.blit(text, (x, y))
            text = font.render(f'Gesture: {hand.gesture}', 1, pygame.Color('black'), pygame.Color('white'))
            screen.blit(text, (x, y + 24))

        pygame.display.flip()
        clock.tick(60)

    gesture_recognizer.stop()
    capture_device.close_camera()
    pygame.quit()
