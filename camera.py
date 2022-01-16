import pygame
from helicopter import Helicopter
from enemy import Enemy


class Camera:
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if isinstance(obj, Helicopter):
            obj.x += self.dx
            obj.y += self.dy
        if isinstance(obj, Enemy):
            obj.x += self.dx
            obj.y += self.dy

    def update(self, target):
        if target is None:
            return
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)
        x = 0