import pygame

import os
import sys

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

tile_width = 20
tile_height = 20

class Person(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = load_image('person-hands-down.png')
        self.frames = []
        self.frames.append(self.image)
        self.frames.append(load_image('person-hands-up.png'))
        self.current_frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * tile_width
        self.rect.y = pos[1] * tile_height
        self.update_count = 0

    def update(self, timedelta, persons_sprite, all_sprites):
        timedelta /= 1000
        self.update_count = (self.update_count + 1) % 60
        if self.update_count == 30:
            self.current_frame = (self.current_frame + 1) % 2
            self.image = self.frames[self.current_frame]

