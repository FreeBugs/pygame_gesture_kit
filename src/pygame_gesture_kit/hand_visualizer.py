import pygame.draw

from .hand import Hand


def draw_bones(surface: pygame.Surface,
               hand: Hand,
               color=(255, 255, 255, 255), width=2, joint_radius=4,
               joint_label_font: pygame.font.Font = None, joint_label_color: pygame.Color = pygame.Color('white')):
    if hand.landmarks is not None and len(hand.landmarks) == 21:
        pygame.draw.lines(surface, color, False, hand.landmarks[0:5], width)
        pygame.draw.lines(surface, color, False, hand.landmarks[5:9], width)
        pygame.draw.lines(surface, color, False, hand.landmarks[9:13], width)
        pygame.draw.lines(surface, color, False, hand.landmarks[13:17], width)
        pygame.draw.lines(surface, color, False, hand.landmarks[17:21], width)
        pygame.draw.lines(surface, color, True,
                          [hand.landmarks[0], hand.landmarks[5], hand.landmarks[9], hand.landmarks[13],
                           hand.landmarks[17]], width)
        for c, i in zip(hand.landmarks, range(22)):
            pygame.draw.circle(surface, color, c, joint_radius)
            if joint_label_font is not None:
                text = joint_label_font.render(f'{i}', 1, joint_label_color)
                surface.blit(text, c)
