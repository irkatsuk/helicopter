import pygame
import os
import sys
import sqlite3
from helicopter import Helicopter
from person import Person
from board import Board
from camera import Camera
from enemy import Enemy

MYEVENTTYPE = pygame.USEREVENT + 1

COLOR_INACTIVE = pygame.Color('white')
COLOR_ACTIVE = pygame.Color('green')

user = 'guest'

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.FONT = pygame.font.Font(None, 32)
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.finish = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.finish = True
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def top_players():
    con = sqlite3.connect('data/score.sqlite')
    cur = con.cursor()
    result = cur.execute("""SELECT user, score FROM score
                            ORDER BY score DESC
                             """).fetchall()
    con.close()
    return result[:3]

def start_screen():
    global user
    fon = pygame.transform.scale(load_image('start.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    input_box = InputBox(280, 50, 140, 32)
    name_text = f"Вертолет-спасатель"
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(name_text, 1, pygame.Color('white'))
    name_rect = string_rendered.get_rect()
    name_rect.x = 70
    name_rect.y = 400
    enter_text = f"Press Enter to start"
    font = pygame.font.Font(None, 30)
    string_rendered_enter = font.render(enter_text, 1, pygame.Color('white'))
    enter_rect = string_rendered_enter.get_rect()
    enter_rect.x = 140
    enter_rect.y = 450
    nick_text = f"Nick:"
    font = pygame.font.Font(None, 30)
    string_rendered_nick = font.render(nick_text, 1, pygame.Color('white'))
    nick_rect = string_rendered_nick.get_rect()
    nick_rect.x = 220
    nick_rect.y = 60
    top_players_text = f"Top players:"
    font = pygame.font.Font(None, 30)
    string_rendered_top_players = font.render(top_players_text, 1,
                                              pygame.Color('white'))
    top_players_rect = string_rendered_top_players.get_rect()
    top_players_rect.x = 280
    top_players_rect.y = 100
    top = top_players()
    font = pygame.font.Font(None, 30)
    top_rendered = []
    for i, el in enumerate(top):
        nick = el[0]
        score = el[1]
        text = f"{i + 1}.{nick} - {score}"
        string_rendered_top = font.render(text, 1, pygame.Color('white'))
        top_rect = string_rendered_top.get_rect()
        top_rect.x = 280
        top_rect.y = 140 + i * 40
        top_rendered.append((string_rendered_top, top_rect))

    while True:

        for event in pygame.event.get():
            input_box.handle_event(event)
            if event.type == pygame.QUIT:
                terminate()
        input_box.update()
        if input_box.finish:
            if len(input_box.text) > 0:
                user = input_box.text
            return
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, name_rect)
        screen.blit(string_rendered_enter, enter_rect)
        screen.blit(string_rendered_nick, nick_rect)
        screen.blit(string_rendered_top_players, top_players_rect)
        for el in top_rendered:
            screen.blit(el[0], el[1])
        input_box.draw(screen)

        pygame.display.flip()

def game_over_screen():
    fon = pygame.transform.scale(load_image('game-over.jpg'), size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()

def win_screen():
    fon = pygame.transform.scale(load_image('you-win.jpg'), size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()

def save_results(user, score):
    con = sqlite3.connect('data/score.sqlite')
    cur = con.cursor()
    result = cur.execute("""SELECT user, score FROM score
                            WHERE user = ?
                         """, (user,)).fetchall()
    if len(result) == 0:
        cur.execute("""INSERT INTO score(user, score) 
                       VALUES(?, ?)""", (user, score)).fetchall()
    else:
        old_score = result[0][1]
        if old_score < score:
            cur.execute("""UPDATE score
                         SET score = ?
                         WHERE user = ?""", (score, user)).fetchall()
    con.commit()
    con.close()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Вертолет-спасатель')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    start_screen()
    maps = ['level1.txt', 'level2.txt', 'level3.txt']
    current_map = 0
    lose = False
    current_score = 0
    while not lose:
        all_sprites = pygame.sprite.Group()
        helicopter_sprite = pygame.sprite.Group()
        persons_sprite = pygame.sprite.Group()
        walls_sprite = pygame.sprite.Group()
        enemy_sprite = pygame.sprite.Group()
        border_sprite = pygame.sprite.Group()
        clock = pygame.time.Clock()
        enemy = Enemy(300, 300)
        enemy_sprite.add(enemy)
        all_sprites.add(enemy)
        enemy = Enemy(300, 350)
        enemy_sprite.add(enemy)
        all_sprites.add(enemy)
        board = Board(width, height, walls_sprite, all_sprites, persons_sprite,
                      enemy_sprite, helicopter_sprite, border_sprite,
                      maps[current_map], current_score)
        camera = Camera(width, height)
        pygame.time.set_timer(MYEVENTTYPE, 1000)
        running = True
        while running:
            timedelta = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    terminate()
                if event.type == MYEVENTTYPE:
                    board.fuel_down()
                    pygame.time.set_timer(MYEVENTTYPE, 1000)
            screen.fill(('cadetblue1'))
            camera.update(board.get_helicopter())
            for sprite in all_sprites:
                camera.apply(sprite)
            walls_sprite.update()
            walls_sprite.draw(screen)
            board.update()
            all_sprites.update(timedelta, persons_sprite, all_sprites)
            all_sprites.draw(screen)
            board.draw(screen)
            if board.end() == 'lose' or board.end() == 'win':
                break
            pygame.display.flip()
        save_results(user, board.get_score())
        current_score = board.get_score()
        if board.end() == 'lose':
            game_over_screen()
            terminate()
        elif board.end() == 'win':
            win_screen()
            current_map = (current_map + 1) % len(maps)
    pygame.quit()
