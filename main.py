import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


''' будущая анимация
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, imgs, x, y):
        super().__init__(all_sprites)
        self.frames = imgs[:]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(100, 100, x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
'''


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen(screen):
    intro_text = ["Civil defense"]
    fon = pygame.transform.scale(load_image('fon1.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 250
    for line in intro_text:
        string_rendered = my_font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                # terminate()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except Exception:
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    return level_map


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type in ['wall_left', 'wall_right', 'side_left', 'side_right', 'top_left', 'top_right', 'down_left',
                         'down_right']:
            super().__init__(all_sprites, wall_group)
        elif tile_type == "floor":
            super().__init__(all_sprites, floor_group)
        # im = tile_images[tile_type]
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'elf':
            super().__init__(hero_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - (tile_height / 7 * 4))


'''class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'elf':
            super().__init__(hero_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - (tile_height / 7 * 4))
'''


class UI(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        self.tile_type = tile_type
        if tile_type == 'close':
            super().__init__(all_sprites, ui_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(x, y)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'e':
                Tile('empty', x, y)
            elif level[y][x] == 'wl':
                Tile('wall_left', x, y)
            elif level[y][x] == 'wr':
                Tile('wall_right', x, y)
            elif level[y][x] == 'sl':
                Tile('side_left', x, y)
            elif level[y][x] == 'sr':
                Tile('side_right', x, y)
            elif level[y][x] == 'dl':
                Tile('down_left', x, y)
            elif level[y][x] == 'dr':
                Tile('down_right', x, y)
            elif level[y][x] == 'f':
                Tile('floor', x, y)
            elif level[y][x] == 'H':
                Tile('floor', x, y)
                Hero('elf', x, y)


FPS = 50
clock = pygame.time.Clock()

if __name__ in '__main__':
    filename = 'level1.txt'
    level_map = load_level(filename)
    level_map = [el.split() for el in level_map]

    pygame.init()
    my_font = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    size = screen.get_size()
    width, height = size

    start_screen(screen)

    tile_width = tile_height = 40

    tile_images = {
        'floor': pygame.transform.scale(load_image('floor_1.png'), (tile_width, tile_height)),
        'wall_left': pygame.transform.scale(load_image('wall_left.png'), (tile_width, tile_height)),
        'wall_right': pygame.transform.scale(load_image('wall_right.png'), (tile_width, tile_height)),
        'side_left': pygame.transform.scale(load_image('wall_side_mid_left.png'), (tile_width, tile_height)),
        'side_right': pygame.transform.scale(load_image('wall_side_mid_right.png'), (tile_width, tile_height)),
        'down_left': pygame.transform.scale(load_image('down_left.png'), (tile_width, tile_height)),
        'down_right': pygame.transform.scale(load_image('down_right.png'), (tile_width, tile_height)),
        'empty': pygame.transform.scale(load_image('black.png'), (tile_width, tile_height)),
        'close': pygame.transform.scale(load_image('close.png'), (tile_width, tile_height)),
        'elf': pygame.transform.scale(load_image('elf_f_idle_anim_f0.png'),
                                      (tile_width, tile_height + (tile_height / 7 * 4))),
    }

    all_sprites = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    ui_group = pygame.sprite.Group()
    UI('close', width - tile_width - 50, 50)

    generate_level(level_map)

    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [el for el in ui_group if el.rect.collidepoint(pos)]
                for el in clicked_sprites:
                    if el.tile_type == 'close':
                        terminate()
        all_sprites.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
    terminate()
