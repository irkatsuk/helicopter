import pygame
import os
import sys
from person import Person
from enemy import Enemy
from helicopter import Helicopter

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '0'), level_map))

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

tile_width = 20
tile_height = 20

class TileWater(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((tile_width, tile_height))
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class TileSand(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((tile_width, tile_height))
        self.image.fill(pygame.Color('yellow'))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class TileSpace(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((tile_width, tile_height))
        self.image.fill(pygame.Color('darkslateblue'))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class TileSwamp(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((tile_width, tile_height))
        self.image.fill(pygame.Color('chartreuse4'))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class TileBorder(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((tile_width, tile_height))
        self.image.fill(pygame.Color('cadetblue1'))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class TileGround(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = None
        if tile_type == 'ground':
            self.image = load_image("ground.png")
        elif tile_type == 'left':
            self.image = load_image("left-ground.png")
        else:
            self.image = load_image("right-ground.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image("tower.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Balloon(pygame.sprite.Sprite):
    def __init__(self, frame, pos_x, pos_y):
        super().__init__()
        self.frames = []
        self.sheet1 = load_image("air-balloon1.png")
        self.frames.append(self.sheet1)
        self.sheet2 = load_image("air-balloon2.png")
        self.frames.append(self.sheet2)
        self.sheet3 = load_image("air-balloon3.png")
        self.frames.append(self.sheet3)

        self.cur_frame = frame
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y

class Board:
    def __init__(self, width, height, walls_sprite, all_sprites,
                 persons_sprite, enemy_sprite, helicopter_sprite, border_sprite,
                 map_name, current_score):
        self.width = width
        self.height = height
        self.level_map = load_level(map_name)
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.top_tile = None
        self.walls_sprite = walls_sprite
        self.all_sprites = all_sprites
        self.persons_sprite = persons_sprite
        self.enemy_sprite = enemy_sprite
        self.helicopter_sprite = helicopter_sprite
        self.helicopter = None
        self.border_sprite = border_sprite
        self.score = current_score
        self.man_left = 0
        self.fuel = 100
        self.crash = False
        current_balloon = 0
        for y in range(len(self.level_map)):
            for x in range(len(self.level_map[y])):
                tile = None
                if self.level_map[y][x] == '1':
                    tile = TileWater('empty', x, y)
                    self.walls_sprite.add(tile)
                    self.all_sprites.add(tile)
                elif self.level_map[y][x] == 'x':
                    person = Person((x, y))
                    self.all_sprites.add(person)
                    self.persons_sprite.add(person)
                    self.man_left += 1
                elif self.level_map[y][x] == '2':
                    tile = TileSand('empty', x, y)
                    self.walls_sprite.add(tile)
                    self.all_sprites.add(tile)
                elif self.level_map[y][x] == '3':
                    tile = TileSwamp('empty', x, y)
                    self.walls_sprite.add(tile)
                    self.all_sprites.add(tile)
                elif self.level_map[y][x] == '9':
                    tile = TileSpace('empty', x, y)
                    self.walls_sprite.add(tile)
                    self.all_sprites.add(tile)
                elif self.level_map[y][x] == '7':
                    tile = TileBorder('empty', x, y)
                    self.all_sprites.add(tile)
                    self.border_sprite.add(tile)
                elif self.level_map[y][x] == '@':
                    self.helicopter = Helicopter((tile_width * x,
                                                  tile_height * y))
                    self.all_sprites.add(self.helicopter)
                    self.helicopter_sprite.add(self.helicopter)
                elif self.level_map[y][x] == 'h':
                    tower = Tower(x, y)
                    self.border_sprite.add(tower)
                    self.all_sprites.add(tower)
                elif self.level_map[y][x] == 'g':
                    ground = TileGround('ground', x, y)
                    self.border_sprite.add(ground)
                    self.all_sprites.add(ground)
                elif self.level_map[y][x] == 'w':
                    ground = TileGround('left', x, y)
                    self.border_sprite.add(ground)
                    self.all_sprites.add(ground)
                elif self.level_map[y][x] == 'e':
                    ground = TileGround('right ', x, y)
                    self.border_sprite.add(ground)
                    self.all_sprites.add(ground)
                elif self.level_map[y][x] == 'b':
                    balloon = Balloon(current_balloon , x, y)
                    current_balloon = (current_balloon + 1) % 10
                    self.all_sprites.add(balloon)
                    self.walls_sprite.add(balloon)
                if x == 0 and y == 0:
                    self.top_tile = tile

    def get_player_pos(self, x, y):
        offx = self.top_tile.rect.x
        offy = self.top_tile.rect.y
        return (self.cell_size * x + offx + 15, self.cell_size * y + offy + 5)

    def get_cell(self, pos):
        offx = self.top_tile.rect.x
        offy = self.top_tile.rect.y
        x = (pos[0] - self.left - offx) // self.cell_size
        y = (pos[1] - self.top - offy) // self.cell_size
        return (x, y)

    def update(self):
        sprite = pygame.sprite.groupcollide(self.walls_sprite,
                                            self.helicopter_sprite, False, True)
        if sprite is not None and len(sprite) > 0:
            self.crash = True
        sprite = pygame.sprite.groupcollide(self.border_sprite,
                                            self.helicopter_sprite,
                                            False, False)
        if sprite is not None and len(sprite) > 0:
            for border in sprite:
                rect = border.rect
                player = sprite[border]
                player = player[0]
                collide =  rect.collidepoint(player.rect.midright)
                if collide:
                    player.rect.x -= 1
                    player.x -= 1
                    break
                collide =  rect.collidepoint(player.rect.midleft)
                if collide:
                    player.rect.x += 1
                    player.x += 1
                    break
                collide =  rect.collidepoint(player.rect.midbottom)
                if collide:
                    player.rect.y -= 1
                    player.y -= 1
                    break

        sprite = pygame.sprite.groupcollide(self.persons_sprite,
                                            self.helicopter_sprite, True, False)
        if sprite is not None and len(sprite) > 0:
            self.man_left -= len(sprite)
            self.score += 10 * len(sprite)
        sprite = pygame.sprite.groupcollide(self.enemy_sprite,
                                            self.helicopter_sprite, True, True)
        if sprite is not None and len(sprite) > 0:
            self.crash = True
        sprite = pygame.sprite.groupcollide(self.enemy_sprite,
                                            self.walls_sprite,
                                            False, False)
        if sprite is not None and len(sprite) > 0:
            for enemy in sprite:
                enemy.vy = -enemy.vy
                break
        sprite = pygame.sprite.groupcollide(self.enemy_sprite,
                                            self.border_sprite,
                                            False, False)
        if sprite is not None and len(sprite) > 0:
            for enemy in sprite:
                enemy.vx = -enemy.vx
                break

    def draw(self, screen):
        score_text = f"Score: {self.score}"
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(score_text, 1, pygame.Color('white'))
        score_rect = string_rendered.get_rect()
        score_rect.x = 10
        score_rect.y = 10
        screen.blit(string_rendered, score_rect)
        man_left_text = f"Man left: {self.man_left}"
        string_rendered = font.render(man_left_text, 1, pygame.Color('white'))
        man_left_rect = string_rendered.get_rect()
        man_left_rect.x = 10
        man_left_rect.y = 40
        screen.blit(string_rendered, man_left_rect)
        fuel_text = f"Fuel: {self.fuel}"
        string_rendered = font.render(fuel_text, 1, pygame.Color('white'))
        fuel_rect = string_rendered.get_rect()
        fuel_rect.x = self.width - 100
        fuel_rect.y = 10
        screen.blit(string_rendered, fuel_rect)

    def fuel_down(self):
        self.fuel -= 1

    def end(self):
        if self.fuel == 0 or self.crash:
            return 'lose'
        if self.man_left == 0:
            return 'win'
        return 'continue'

    def get_score(self):
        return self.score + self.fuel

    def get_helicopter(self):
        return self.helicopter

