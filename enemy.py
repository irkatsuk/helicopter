import pygame

import os
import sys

def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('rocket1-left.png')
        self.left_frames = []
        self.left_frames.append(self.image)
        self.left_frames.append(load_image('rocket2-left.png'))
        self.right_frames = []
        self.right_frames.append(load_image('rocket1-right.png'))
        self.right_frames.append(load_image('rocket2-right.png'))
        self.current_frame = 0
        self.rect = self.image.get_rect()
        self.vx = 1
        self.vy = 1
        if self.vx > 0:
            self.image = self.right_frames[self.current_frame]
        else:
            self.image = self.left_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.step = 25
        self.update_count = 0

    def update(self, timedelta, persons_sprite, all_sprites):
        timedelta /= 1000
        self.update_count = (self.update_count + 1) % 60
        if self.update_count == 30:
            self.current_frame = (self.current_frame + 1) % 2
            if self.vx > 0:
                self.image = self.right_frames[self.current_frame]
            else:
                self.image = self.left_frames[self.current_frame]

        vx = self.step * timedelta * self.vx
        vy = self.step * timedelta * self.vy
        self.x += vx
        self.y += vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
