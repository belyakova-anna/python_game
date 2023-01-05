import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


class AnimatedPortal(pygame.sprite.Sprite):
    def __init__(self, num, x, y):
        super().__init__(level_sprites, portal_group)
        if num == 1:
            self.frames = [pygame.transform.scale(load_image('11.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('21.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('31.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('41.png'), (tile_width, tile_height))]
        elif num == 2:
            self.frames = [pygame.transform.scale(load_image('12.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('22.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('32.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('42.png'), (tile_width, tile_height))]
        elif num == 3:
            self.frames = [pygame.transform.scale(load_image('13.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('23.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('33.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('43.png'), (tile_width, tile_height))]
        elif num == 4:
            self.frames = [pygame.transform.scale(load_image('14.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('24.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('34.png'), (tile_width, tile_height)),
                           pygame.transform.scale(load_image('44.png'), (tile_width, tile_height))]
        self.cur_frame = 0
        self.image = self.frames[int(self.cur_frame)]
        self.rect = pygame.Rect(tile_width * x, tile_height * y, tile_width, tile_height)

    def update(self):
        self.cur_frame = (self.cur_frame + 0.05) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]


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


def home_screen(screen):
    font1 = pygame.font.Font('data/Undertale-Battle-Font.ttf', 20)

    # Create a font file by passing font file
    # and size of the font
    text1 = font1.render('Некромант', True, (255, 255, 255))
    textRect1 = text1.get_rect()
    while True:
        screen.fill(pygame.Color('black'))
        home_sprites.draw(screen)
        hero_group.draw(screen)
        if hero.cur_scene == 'level':
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # terminate()
                return  # начинаем игру
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hero.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    hero.move(1, 0)
                elif event.key == pygame.K_UP:
                    hero.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    hero.move(0, 1)
        if (abs(hero.rect[0] - necromancer.rect[0]) <= tile_width) and (
                abs(hero.rect[1] - necromancer.rect[1]) <= tile_height):
            textRect1.center = (necromancer.rect[0] + text1.get_rect()[2] // 4, necromancer.rect[1])
            screen.blit(text1, textRect1)
        pygame.display.flip()


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except Exception:
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    return level_map


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(level_sprites, box_group)
        self.image = tile_images['box']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type in ['wall_left', 'wall_right', 'side_left', 'side_right', 'top_left', 'top_right', 'down_left',
                         'down_right']:
            super().__init__(level_sprites, wall_group)
        elif tile_type == 'wall_home':
            super().__init__(home_sprites, wall_home_group)
        elif tile_type in ['floor_home', 'cover1', 'cover2', 'cover3', 'cover4', 'cover5',
                           'cover6', 'cover7', 'cover8']:
            super().__init__(home_sprites, floor_home_group)
        elif tile_type == 'floor_fon':
            super().__init__(level_sprites)
        elif tile_type == 'floor_home_fon':
            super().__init__(home_sprites)
        elif tile_type in ['exit_left', 'exit_right']:
            super().__init__(home_sprites, exit_group, floor_home_group)
        elif tile_type in ['necromancer', 'okult1', 'okult2', 'okult3', 'okult4']:
            super().__init__(home_sprites, necromancer_group)
        elif tile_type == "floor":
            super().__init__(level_sprites, floor_group)
        # im = tile_images[tile_type]
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Necromancer(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(home_sprites, necromancer_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'elf':
            super().__init__(hero_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.rotation = 'right'

    def move(self, dx, dy):
        if self.cur_scene == 'home':
            all_right = 1
            for el in home_sprites:
                el.rect = pygame.rect.Rect(el.rect[0] - dx * tile_width, el.rect[1] - dy * tile_height,
                                           el.rect[2],
                                           el.rect[3])
            if pygame.sprite.spritecollideany(self, exit_group):
                self.cur_scene = 'level'
            if self.cur_scene == 'home' and not pygame.sprite.spritecollideany(self, floor_home_group):
                all_right = 0
                for el in home_sprites:
                    el.rect = pygame.rect.Rect(el.rect[0] + dx * tile_width, el.rect[1] + dy * tile_height,
                                               el.rect[2],
                                               el.rect[3])
            if dx == -1 and self.rotation == 'right' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'left'
            elif dx == 1 and self.rotation == 'left' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'right'
        if self.cur_scene == 'level':
            all_right = 1
            for el in level_sprites:
                el.rect = pygame.rect.Rect(el.rect[0] - dx * tile_width, el.rect[1] - dy * tile_height,
                                           el.rect[2],
                                           el.rect[3])
            if not pygame.sprite.spritecollideany(self, floor_group):
                all_right = 0
                for el in level_sprites:
                    el.rect = pygame.rect.Rect(el.rect[0] + dx * tile_width, el.rect[1] + dy * tile_height,
                                               el.rect[2],
                                               el.rect[3])
            if dx == -1 and self.rotation == 'right' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'left'
            elif dx == 1 and self.rotation == 'left' and all_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rotation = 'right'


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
            super().__init__(ui_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(x, y)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'H':
                center = [x, y]
    x_screen = width // tile_width
    y_screen = height // tile_height
    x_screen_center = x_screen // 2
    y_screen_center = y_screen // 2
    dx = x_screen_center - center[0]
    dy = y_screen_center - center[1]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'e':
                Tile('empty', x + dx, y + dy)
            elif level[y][x] == 'wl':
                Tile('wall_left', x + dx, y + dy)
            elif level[y][x] == 'wr':
                Tile('wall_right', x + dx, y + dy)
            elif level[y][x] == 'sl':
                Tile('side_left', x + dx, y + dy)
            elif level[y][x] == 'sr':
                Tile('side_right', x + dx, y + dy)
            elif level[y][x] == 'dl':
                Tile('down_left', x + dx, y + dy)
            elif level[y][x] == 'dr':
                Tile('down_right', x + dx, y + dy)
            elif level[y][x] == 'f':
                Tile('floor', x + dx, y + dy)
            elif level[y][x] == 'H':
                Tile('floor', x + dx, y + dy)
                hero.rect = pygame.rect.Rect((x + dx) * tile_width, (y + dy) * tile_height,
                                             hero.rect[2],
                                             hero.rect[3])
            elif level[y][x] == 'p1':
                Tile('floor', x + dx, y + dy)
                AnimatedPortal(1, x + dx, y + dy)
            elif level[y][x] == 'p2':
                Tile('floor', x + dx, y + dy)
                AnimatedPortal(2, x + dx, y + dy)
            elif level[y][x] == 'p3':
                Tile('floor', x + dx, y + dy)
                AnimatedPortal(3, x + dx, y + dy)
            elif level[y][x] == 'p4':
                Tile('floor', x + dx, y + dy)
                AnimatedPortal(4, x + dx, y + dy)
            elif level[y][x] == 'b':
                Tile('floor_fon', x + dx, y + dy)
                Box(x + dx, y + dy)
    # return hero


def generate_home(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'H':
                center = [x, y]
    x_screen = width // tile_width
    y_screen = height // tile_height
    x_screen_center = x_screen // 2
    y_screen_center = y_screen // 2
    dx = x_screen_center - center[0]
    dy = y_screen_center - center[1]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'f':
                Tile('floor_home', x + dx, y + dy)
            elif level[y][x] == 'w':
                Tile('wall_home', x + dx, y + dy)
            elif level[y][x] == 'el':
                Tile('exit_left', x + dx, y + dy)
            elif level[y][x] == 'er':
                Tile('exit_right', x + dx, y + dy)
            elif level[y][x] == 'c1':
                Tile('cover1', x + dx, y + dy)
            elif level[y][x] == 'c2':
                Tile('cover2', x + dx, y + dy)
            elif level[y][x] == 'c3':
                Tile('cover3', x + dx, y + dy)
            elif level[y][x] == 'c4':
                Tile('cover4', x + dx, y + dy)
            elif level[y][x] == 'c5':
                Tile('cover5', x + dx, y + dy)
            elif level[y][x] == 'c6':
                Tile('cover6', x + dx, y + dy)
            elif level[y][x] == 'c7':
                Tile('cover7', x + dx, y + dy)
            elif level[y][x] == 'c8':
                Tile('cover8', x + dx, y + dy)
            elif level[y][x] == 'H':
                Tile('floor_home', x + dx, y + dy)
                hero = Hero('elf', x + dx, y + dy)
            elif level[y][x] == 'N':
                Tile('floor_home_fon', x + dx, y + dy)
                necromancer = Necromancer('necromancer', x + dx, y + dy)
            elif level[y][x] == 'o1':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult1', x + dx, y + dy)
            elif level[y][x] == 'o2':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult2', x + dx, y + dy)
            elif level[y][x] == 'o3':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult3', x + dx, y + dy)
            elif level[y][x] == 'o4':
                Tile('floor_home_fon', x + dx, y + dy)
                Tile('okult4', x + dx, y + dy)
    return hero, necromancer


if __name__ in '__main__':
    pygame.init()
    my_font = pygame.font.Font('data/Undertale-Battle-Font.ttf', 50)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # screen = pygame.display.set_mode((500, 500))
    size = screen.get_size()
    width, height = size

    start_screen(screen)

    tile_width = tile_height = 60
    tile_images = {
        'floor': pygame.transform.scale(load_image('floor_1.png'), (tile_width, tile_height)),
        'floor_fon': pygame.transform.scale(load_image('floor_1.png'), (tile_width, tile_height)),
        'wall_left': pygame.transform.scale(load_image('wall_left.png'), (tile_width, tile_height)),
        'wall_right': pygame.transform.scale(load_image('wall_right.png'), (tile_width, tile_height)),
        'side_left': pygame.transform.scale(load_image('wall_side_mid_left.png'), (tile_width, tile_height)),
        'side_right': pygame.transform.scale(load_image('wall_side_mid_right.png'), (tile_width, tile_height)),
        'down_left': pygame.transform.scale(load_image('down_left.png'), (tile_width, tile_height)),
        'down_right': pygame.transform.scale(load_image('down_right.png'), (tile_width, tile_height)),
        'empty': pygame.transform.scale(load_image('black.png'), (tile_width, tile_height)),
        'close': pygame.transform.scale(load_image('close.png'), (tile_width, tile_height)),
        'elf': pygame.transform.scale(load_image('elf_square.png'),
                                      (tile_width, tile_height)),
        'wall_home': pygame.transform.scale(load_image('wall.png'), (tile_width, tile_height)),
        'floor_home': pygame.transform.scale(load_image('floor_home.png'), (tile_width, tile_height)),
        'floor_home_fon': pygame.transform.scale(load_image('floor_home.png'), (tile_width, tile_height)),
        'exit_left': pygame.transform.scale(load_image('exit_left.png'), (tile_width, tile_height)),
        'exit_right': pygame.transform.scale(load_image('exit_right.png'), (tile_width, tile_height)),
        'cover1': pygame.transform.scale(load_image('cover1.png'), (tile_width, tile_height)),
        'cover2': pygame.transform.scale(load_image('cover2.png'), (tile_width, tile_height)),
        'cover3': pygame.transform.scale(load_image('cover3.png'), (tile_width, tile_height)),
        'cover4': pygame.transform.scale(load_image('cover4.png'), (tile_width, tile_height)),
        'cover5': pygame.transform.scale(load_image('cover5.png'), (tile_width, tile_height)),
        'cover6': pygame.transform.scale(load_image('cover6.png'), (tile_width, tile_height)),
        'cover7': pygame.transform.scale(load_image('cover7.png'), (tile_width, tile_height)),
        'cover8': pygame.transform.scale(load_image('cover8.png'), (tile_width, tile_height)),
        'necromancer': pygame.transform.scale(load_image('necromancer_idle_anim_f1.png'), (tile_width, tile_height)),
        'okult1': pygame.transform.scale(load_image('okult1.png'), (tile_width, tile_height)),
        'okult2': pygame.transform.scale(load_image('okult2.png'), (tile_width, tile_height)),
        'okult3': pygame.transform.scale(load_image('okult3.png'), (tile_width, tile_height)),
        'okult4': pygame.transform.scale(load_image('okult4.png'), (tile_width, tile_height)),
        'box': pygame.transform.scale(load_image('chest_empty_open_anim_f0.png'), (tile_width, tile_height)),
    }

    home_sprites = pygame.sprite.Group()
    wall_home_group = pygame.sprite.Group()
    floor_home_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    necromancer_group = pygame.sprite.Group()

    level_sprites = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    ui_group = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()

    filename = 'home.txt'
    home_map = load_level(filename)
    home_map = [el.split() for el in home_map]
    hero, necromancer = generate_home(home_map)
    hero.cur_scene = 'home'
    home_screen(screen)

    filename = 'level1.txt'
    level_map = load_level(filename)
    level_map = [el.split() for el in level_map]
    hero.cur_scene = 'level'
    generate_level(level_map)

    close = UI('close', width - tile_width - 50, 50)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hero.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    hero.move(1, 0)
                elif event.key == pygame.K_UP:
                    hero.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    hero.move(0, 1)

        # portal_group.update()
        # portal_group.draw(screen)

        level_sprites.update()
        level_sprites.draw(screen)
        hero_group.draw(screen)
        ui_group.draw(screen)
        pygame.display.flip()
    terminate()
