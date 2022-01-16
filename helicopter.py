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

class Helicopter(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.sheet = load_image("helicopter-sprite2.png")
        self.columns = 7
        self.rows = 6
        self.frames = []
        self.updateFrame = 0
        self.current_row = 0
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.vy = 50
        self.step = 50
        self.x = self.rect.x
        self.y = self.rect.y
        self.res = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self, pos):
        self.rect.x = pos[0]
        self.x = self.rect.x
        self.rect.y = pos[1]
        self.y = self.rect.y

    def update(self, timedelta, persons_sprite, all_sprites):
        timedelta /= 1000
        vx = 0
        vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            vx = -self.step * timedelta
            self.current_row = 1
        if keys[pygame.K_RIGHT]:
            vx = self.step * timedelta
            self.current_row = 0
        if keys[pygame.K_UP]:
            vy = -self.step * timedelta
        if keys[pygame.K_DOWN]:
            vy = self.step * timedelta

        self.updateFrame = (self.updateFrame + 1) % 60
        if self.updateFrame % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % self.columns  + \
                             self.current_row * self.columns
            self.image = self.frames[self.cur_frame]

        self.x += vx
        self.y += vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
