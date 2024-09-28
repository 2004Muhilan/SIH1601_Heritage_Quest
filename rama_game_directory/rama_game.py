import pygame
import sys
import random
import moviepy.editor as mp
import threading
from PIL import Image
import os
import math


def __main__():
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Initialization of main variables
    pygame.init()

    # Screen width and height
    WIDTH = 1280
    HEIGHT = 720

    # Screen (display) and clock (fps)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Game level and state and intro (whether the level has been opened for the first time)
    game_level = 5
    game_state, intro = False, True

    # Font for rendering stuff, you can change it to custom later if necessary
    font = pygame.font.Font(None, 36)

    # Level 1 classes ======================================================================================================

    class Level_1_Rama(pygame.sprite.Sprite):

        gravity = 0
        distances = 0
        jumps = 0

        def __init__(self):
            super().__init__()
            self.player_walk = []
            for i in range(1, 7):
                self.player_walk.append(pygame.transform.rotozoom(
                    pygame.image.load(os.path.join(base_path, f'./level 1/images/rama/rama_running_{i}.png')).convert_alpha(), 0, 1))
            self.player_index = 0
            self.player_jump_image = pygame.transform.rotozoom(
                pygame.image.load(os.path.join(base_path, './level 1/images/rama/rama_jumping.png')).convert_alpha(), 0, 1)
            self.jumped = False
            self.image = self.player_walk[self.player_index]
            self.y = 675
            self.rect = self.image.get_rect(topleft=(50, self.y))
            self.rect = self.rect.inflate(-20, 0)

        def get_distance(self, enemies_group):
            closest_distance = float('inf')
            closest_enemy = None
            for enemy in enemies_group:
                distance = math.sqrt((enemy.rect.centerx - self.rect.centerx) ** 2 + (enemy.rect.centery - self.rect.centery) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy

            if closest_enemy:
                Level_1_Rama.distances += closest_distance

        def player_input(self, enemies_group):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.jumped is False:
                self.get_distance(enemies_group)
                self.jumped = True
                Level_1_Rama.jumps += 1
                Level_1_Rama.gravity = -20

        def gravity_apply(self):
            if self.jumped:
                self.rect.y += Level_1_Rama.gravity
                Level_1_Rama.gravity += 1
            if self.rect.bottom >= self.y:
                self.jumped = False
                self.rect.bottom = self.y

        def animation_state(self):
            if self.rect.bottom < self.y:
                self.image = self.player_jump_image
            else:
                self.player_index += 0.125
                if self.player_index >= 6:
                    self.player_index = 0
                self.image = self.player_walk[int(self.player_index)]

        def reset_gravity(self):
            self.gravity = 0

        def update(self, enemies_group):
            self.player_input(enemies_group)
            self.gravity_apply()
            self.animation_state()

    class Level_1_Enemy(pygame.sprite.Sprite):

        enemy_speed = 9

        def __init__(self, ring):
            super().__init__()

            if random.choice([1, 2, 2]) == 2:
                enemy_walk1 = pygame.transform.rotozoom(
                    pygame.image.load(os.path.join(base_path, './level 1/images/enemies/Snake/snake_1.png')).convert_alpha(), 0, 0.25)
                enemy_walk2 = pygame.transform.rotozoom(
                    pygame.image.load(os.path.join(base_path, './level 1/images/enemies/Snake/snake_2.png')).convert_alpha(), 0, 0.25)
                enemy_walk3 = pygame.transform.rotozoom(
                    pygame.image.load(os.path.join(base_path, './level 1/images/enemies/Snake/snake_3.png')).convert_alpha(), 0, 0.25)
                y_pos = 675
                self.enemy_walk = [enemy_walk1, enemy_walk2, enemy_walk3]
            else:
                enemy_walk1 = pygame.transform.rotozoom(
                    pygame.image.load(os.path.join(base_path, './level 1/images/enemies/bat_1.png')).convert_alpha(), 0, 0.4)
                enemy_walk2 = pygame.transform.rotozoom(
                    pygame.image.load(os.path.join(base_path, './level 1/images/enemies/bat_2.png')).convert_alpha(), 0, 0.4)
                enemy_walk3 = pygame.transform.rotozoom(
                    pygame.image.load(os.path.join(base_path, './level 1/images/enemies/bat_3.png')).convert_alpha(), 0, 0.4)
                y_pos = 400
                self.enemy_walk = [enemy_walk1, enemy_walk2, enemy_walk3]

            self.enemy_index = 0
            self.image = self.enemy_walk[self.enemy_index]
            self.rect = self.image.get_rect(bottomleft=(WIDTH + 10, y_pos)).inflate(-60, -40)

        def movement(self):
            if self.rect.right >= 0:
                self.rect.left -= Level_1_Enemy.enemy_speed
            else:
                self.kill()

        def animation_state(self):
            self.enemy_index += 0.1
            if self.enemy_index >= len(self.enemy_walk):
                self.enemy_index = 0
            self.image = self.enemy_walk[int(self.enemy_index)]

        def draw_rect_border(self, screen):
            """Draw the border of the rect on the screen."""
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

        def update(self):
            self.movement()
            self.animation_state()

    class Level_1_Ring(pygame.sprite.Sprite):

        ring_speed = 9

        def __init__(self, ring):
            super().__init__()
            self.image = pygame.transform.rotozoom(
                pygame.image.load(os.path.join(base_path, f'./level 1/images/rings/ring_{ring}.png')).convert_alpha(),
                0, 0.25)
            y_pos = random.randint(400, 675)
            self.rect = self.image.get_rect(bottomleft=(WIDTH + 10, y_pos))
            self.ring = True

        def movement(self):
            if self.rect.right >= 0:
                self.rect.left -= Level_1_Ring.ring_speed
            else:
                self.kill()

        def update(self):
            self.movement()

    # Level 2 classes ======================================================================================================

    class Level_2_Bow(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self.index = 0
            self.image_list = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 2/images/bow_stretched.png")), (200, 300)),
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 2/images/bow_released.png")), (200, 300))
            ]
            self.image = self.image_list[self.index]
            self.rect = self.image.get_rect(center=(WIDTH - 90, HEIGHT / 2))

        def input(self):
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.index = 1
                self.launch()

        def reset(self):
            self.index = 0
            self.image = self.image_list[self.index]
            self.rect = self.image.get_rect(center=(WIDTH - 90, HEIGHT / 2))

        def launch(self):
            self.image = self.image_list[self.index]
            self.rect = self.image.get_rect(center=(WIDTH - 90, HEIGHT / 2))
            lvl_2_arrow.launched = True

        def update(self):
            self.input()

    class Level_2_Arrow(pygame.sprite.Sprite):

        def __init__(self):

            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 2/images/arrow.png")),
                                                (175, 150)).convert_alpha()
            self.rect = self.image.get_rect(center=(WIDTH - 95, HEIGHT / 2))
            self.launched = False

        def move(self):
            nonlocal game_state, lvl_2_score, bad_audio, good_audio
            self.rect.x -= 10
            if self.rect.left <= 550:
                self.launched = False
                if lvl_2_wheel.get_hit():
                    lvl_2_score += 1
                    if lvl_2_score < 3:
                        self.rect.center = (WIDTH - 100, HEIGHT / 2)
                        lvl_2_wheel.increase_speed()
                        lvl_2_bow.reset()
                        pygame.mixer.music.load(good_audio[random.randint(0, 3)])
                        pygame.mixer.music.play()
                    else:
                        self.kill()
                        lvl_2_wheel.kill()
                        lvl_2_bow.kill()
                else:
                    pygame.mixer.music.load(bad_audio[random.randint(0, 1)])
                    pygame.mixer.music.play()
                    game_state = False

        def update(self):
            if self.launched:
                self.move()

    class Level_2_Wheel(pygame.sprite.Sprite):

        def __init__(self):

            super().__init__()
            self.image_list = [
                pygame.transform.rotozoom(pygame.image.load(os.path.join(base_path, "./level 2/images/wheel.png")), 0, 1).convert_alpha(),
                pygame.transform.rotozoom(pygame.image.load(os.path.join(base_path, "./level 2/images/wheel.png")), 15, 1).convert_alpha(),
                pygame.transform.rotozoom(pygame.image.load(os.path.join(base_path, "./level 2/images/wheel.png")), 30, 1).convert_alpha(),
                pygame.transform.rotozoom(pygame.image.load(os.path.join(base_path, "./level 2/images/wheel.png")), 45, 1).convert_alpha(),
                pygame.transform.rotozoom(pygame.image.load(os.path.join(base_path, "./level 2/images/wheel.png")), 60, 1).convert_alpha(),
                pygame.transform.rotozoom(pygame.image.load(os.path.join(base_path, "./level 2/images/wheel.png")), 75, 1).convert_alpha(),
            ]
            self.rect_list = []
            for img in self.image_list:
                self.rect_list.append(img.get_rect(center=(400, 400)))
            self.index = 0
            self.image = self.image_list[self.index]
            self.rect = self.rect_list[self.index]
            self.speed = 0.075

        def animate(self):
            self.index += self.speed
            if self.index >= len(self.image_list):
                self.index = 0
            self.image = self.image_list[int(self.index)]
            self.rect = self.rect_list[int(self.index)]

        def increase_speed(self):
            self.speed += 0.025

        def get_hit(self):
            return 4 > self.index >= 1

        def update(self):
            self.animate()

    # Level 3 classes ======================================================================================================

    class Level_3_Background(pygame.sprite.Sprite):

        def __init__(self, pos):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 3/images/bg.jpeg")),
                                                (1984, 1984)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect

    class Level_3_Tile(pygame.sprite.Sprite):

        def __init__(self, pos, groups):
            super().__init__(groups)
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 3/images/wall.png")),
                                                (64, 64)).convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-5, -10)

    class Level_3_Sita(pygame.sprite.Sprite):

        def __init__(self, pos, groups):
            super().__init__(groups)
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 3/images/sita.png")), (64, 64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect

    class Level_3_Flame(pygame.sprite.Sprite):

        def __init__(self, pos, groups):
            super().__init__(groups)
            self.fire_animate = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 3/images/flame_1.png")), (64, 64)).convert_alpha(),
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 3/images/flame_1.png")), (64, 64)).convert_alpha(),
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 3/images/flame_1.png")), (64, 64)).convert_alpha()
            ]
            self.fire_index = 0
            self.image = self.fire_animate[self.fire_index]
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect

        def animate(self):
            self.fire_index += 0.125
            if self.fire_index == 3:
                self.fire_index = 0
            self.image = self.fire_animate[int(self.fire_index)]

        def update(self):
            self.animate()

    class Level_3_Level:

        def __init__(self):

            # getting the display surface
            self.display_surface = pygame.display.get_surface()

            # sprite group initialization
            self.visible_sprites = Level_3_YSortCameraGroup()
            self.obstacle_sprites = pygame.sprite.Group()
            self.fire_sprites = pygame.sprite.Group()

            self.create_map()

        def create_map(self):
            self.bg = Level_3_Background((0, 0))
            for row_index, row in enumerate(Level_3_WORLD_MAP):
                for col_index, col in enumerate(row):
                    x = row_index * Level_3_TILESIZE
                    y = col_index * Level_3_TILESIZE
                    if col == 'x':
                        Level_3_Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                    elif col == 'p':
                        self.player = Level_3_Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                    elif col == 's':
                        self.sita = Level_3_Sita((x, y), [self.visible_sprites])

        def get_visible_sprite_group(self):
            return self.visible_sprites

        def get_fire_sprite_group(self):
            return self.fire_sprites

        def player_sita_collide(self):
            return pygame.sprite.collide_rect(self.player, self.sita)

        def game_end(self):
            self.bg.kill()
            self.player.kill()
            self.sita.kill()
            self.visible_sprites.empty()
            self.obstacle_sprites.empty()
            self.fire_sprites.empty()

        def run(self):
            # update and draw the game
            self.visible_sprites.custom_draw(self.player, self.bg)
            self.visible_sprites.update()

    class Level_3_YSortCameraGroup(pygame.sprite.Group):

        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.half_width = self.display_surface.get_width() / 2
            self.half_height = self.display_surface.get_height() / 2
            self.offset = pygame.math.Vector2(-400, -400)

        def custom_draw(self, player, bg):
            self.offset.x = player.rect.centerx - self.half_width
            self.offset.y = player.rect.centery - self.half_height

            offset_pos = bg.rect.topleft - self.offset
            self.display_surface.blit(bg.image, offset_pos)

            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    class Level_3_Player(pygame.sprite.Sprite):

        def __init__(self, position, groups, obstacle_sprites):

            super().__init__(groups)
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "./level 3/images/hanuman.png")),
                                                (64, 64)).convert_alpha()
            self.rect = self.image.get_rect(topleft=position)
            self.hitbox = self.rect.inflate(0, -26)

            self.speed = 5
            self.direction = pygame.math.Vector2()

            self.obstacle_sprites = obstacle_sprites

            self.current_cords = (int(self.rect.centerx / 64), int(self.rect.centery / 64))
            self.new_cords = (int(self.rect.centerx / 64), int(self.rect.centery / 64))
            self.fire = False

        def input(self):
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.direction.y = -1
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.direction.y = 1
            else:
                self.direction.y = 0

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.direction.x = -1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.direction.x = 1
            else:
                self.direction.x = 0

        def move(self, speed):
            nonlocal lvl_3_fire_tick_start_time, lvl_3_fire_tick, lvl_3_fire_dmg
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
                if self.current_cords != (int(self.rect.centerx / 64), int(self.rect.centery / 64)):
                    self.fire = True
                    self.new_cords = (int(self.rect.centerx / 64), int(self.rect.centery / 64))
                fire_ticks = False
                for sprite in lvl_3_level.get_fire_sprite_group().sprites():
                    if (int(sprite.rect.centerx / 64), int(sprite.rect.centery / 64)) == self.current_cords and not lvl_3_fire_tick:
                        lvl_3_fire_tick_start_time = int(pygame.time.get_ticks() / 1000)
                        lvl_3_fire_tick = True
                        fire_ticks = True
                        break
                    elif (int(sprite.rect.centerx / 64), int(sprite.rect.centery / 64)) == self.current_cords:
                        fire_ticks = True
                        break
                if not fire_ticks and lvl_3_fire_tick:
                    lvl_3_fire_dmg += int(pygame.time.get_ticks() / 1000) - lvl_3_fire_tick_start_time
                    lvl_3_fire_tick = False

            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center

        def collision(self, direction):
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right

            elif direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom

        def set_fire(self):
            for sprite in lvl_3_level.get_fire_sprite_group().sprites():
                if (int(sprite.rect.centerx / 64), int(sprite.rect.centery / 64)) == self.current_cords:
                    self.fire = False
                    self.current_cords = self.new_cords
                    return
            Level_3_Flame((self.current_cords[0] * Level_3_TILESIZE, self.current_cords[1] * Level_3_TILESIZE),[lvl_3_level.get_fire_sprite_group(), lvl_3_level.get_visible_sprite_group()])
            self.fire = False
            self.current_cords = self.new_cords

        def update(self):
            self.input()
            self.move(self.speed)
            if self.fire:
                self.set_fire()

    # Level 4 classes ======================================================================================================

    class Level_4_Cards(pygame.sprite.Sprite):

        def __init__(self, img, pos):

            super().__init__()
            self.index = 0
            self.image_list = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, './level 4/images/blank_card.png')), (128, 64)).convert_alpha(),
                img]
            self.image = self.image_list[self.index]
            self.pos = pos
            self.rect = self.image.get_rect(topleft=self.pos)

        def swap_state(self):
            self.index = (self.index + 1) % 2
            self.image = self.image_list[self.index]
            self.rect = self.image.get_rect(topleft=self.pos)

        def input(self):
            nonlocal lvl_4_mouse_clicked, lvl_4_cards_flipped_count
            global lvl_4_cards_flipped_imgs
            buttons_clicked = pygame.mouse.get_pressed()
            if not buttons_clicked[0]:
                lvl_4_mouse_clicked = False
            if self.index == 0 and not lvl_4_mouse_clicked and buttons_clicked[0] and self.rect.collidepoint(
                    pygame.mouse.get_pos()):
                lvl_4_cards_flipped.append(self)
                lvl_4_mouse_clicked = True
                self.swap_state()
                lvl_4_cards_flipped_count += 1
                if lvl_4_cards_flipped_count == 2:
                    pass

        def update(self):
            self.input()

    # Level 5 classes ======================================================================================================

    _img_width = 100
    _img_height = 75
    _x_start = 50
    _y_start = 100
    _x_gap = 50
    _y_gap = 2
    _lvl_5_static_arrow_image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, './level 5/images/projectiles/arrow.png')), (_img_width, _img_height))
    _lvl_5_static_arrow_img_rects = [_lvl_5_static_arrow_image.get_rect(topleft=(_x_start + (j * _img_width) + (j * _x_gap), _y_start + (i * _img_height) + (i * _y_gap))) for i in range(7, 8) for j in range(0, 8)]

    class Level_5_Rama(pygame.sprite.Sprite):

        arrows = 0

        def __init__(self):
            super().__init__()
            # self.player_walk = [pygame.image.load(os.path.join(base_path, f'./level 5/images/player/rama_running_{i}.png')) for i in range(1, 7)]
            self.player_right_walk = [pygame.image.load(os.path.join(base_path, f'./level 5/images/player/right_rama_running_{i}.png')) for i in range(1, 7)]
            self.player_left_walk = [pygame.image.load(os.path.join(base_path, f'./level 5/images/player/left_rama_running_{i}.png')) for i in range(1, 7)]
            self.player_right_stand = pygame.image.load(os.path.join(base_path, './level 5/images/player/right_rama_standing.png'))
            self.player_left_stand = pygame.image.load(os.path.join(base_path, './level 5/images/player/left_rama_standing.png'))
            self.player_index = 0
            self.direction = 1
            self.velocity = 0
            self.image = self.player_right_walk[self.player_index]
            self.rect = self.image.get_rect(topleft=(50, 475))
            self.rect = self.rect.inflate(-20, 0)

        def player_input(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and keys[pygame.K_d]:
                self.velocity = 0
            elif keys[pygame.K_a]:
                self.direction = -1
                self.velocity = -7
            elif keys[pygame.K_d]:
                self.direction = 1
                self.velocity = 7
            else:
                self.velocity = 0

        def velocity_apply(self):
            self.rect.x += self.velocity

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > 1280:
                self.rect.right = 1280

        def animation_state(self):
            if self.velocity != 0:
                self.player_index += 0.125
                if self.player_index >= 6:
                    self.player_index = 0
                if self.direction == 1:
                    self.image = self.player_right_walk[int(self.player_index)]
                else:
                    self.image = self.player_left_walk[int(self.player_index)]
            else:
                self.player_index = 0
                if self.direction == 1:
                    self.image = self.player_right_stand
                else:
                    self.image = self.player_left_stand

        def update(self):
            self.player_input()
            self.velocity_apply()
            self.animation_state()

    class Level_5_Arrow_Spawn(pygame.sprite.Sprite):

        image = _lvl_5_static_arrow_image
        img_rects = _lvl_5_static_arrow_img_rects

        def __init__(self):
            super().__init__()

            self.image = Level_5_Arrow_Spawn.image
            self.rect = Level_5_Arrow_Spawn.img_rects[random.randint(0, len(Level_5_Arrow_Spawn.img_rects) - 1)]

    class Level_5_Arrow_Shot(pygame.sprite.Sprite):

        def __init__(self, current, target):
            super().__init__()
            original_image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, './level 5/images/projectiles/arrow.png')), (80, 65))
            self.rect = original_image.get_rect(center=current)
            self.target = target
            self.speed = 5

            self.direction = self.get_direction()
            angle = self.calculate_angle()
            self.image = pygame.transform.rotate(original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        def get_direction(self):
            start = self.rect.center
            target = self.target
            dx, dy = target[0] - start[0], target[1] - start[1]
            distance = math.hypot(dx, dy)  # Distance between two points
            if distance == 0:  # Avoid division by zero
                return 0, 0
            return dx / distance, dy / distance  # Return normalized vector

        def calculate_angle(self):
            start = self.rect.center
            target = self.target
            dx, dy = target[0] - start[0], target[1] - start[1]
            angle = math.degrees(math.atan2(-dy, dx))  # Negative dy to account for inverted Y-axis
            return angle + 180

        def apply_speed(self):
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

        def apply_death(self):
            top, bottom, left, right = self.rect.top, self.rect.bottom, self.rect.left, self.rect.right
            if top < 0 or left < 0:
                self.kill()
            elif bottom > HEIGHT or right > WIDTH:
                self.kill()

        def update(self):
            self.apply_speed()
            self.apply_death()

    class Level_5_Indrajith(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, './level 5/images/enemy/indrajith.png')), (175, 175))
            self.rect = self.image.get_rect(center=(WIDTH / 2, 150))
            self.velocity = [-7, 7][random.randint(0, 1)]
            self.left_check = random.randint(0, 200)
            self.right_check = random.randint(WIDTH - 200, WIDTH)

        def change_direction(self):
            if self.rect.left <= self.left_check:
                self.velocity = 7
                self.left_check = random.randint(0, 200)
            elif self.rect.right >= self.right_check:
                self.velocity = -7
                self.right_check = random.randint(WIDTH - 200, WIDTH)

        def apply_velocity(self):
            self.rect.x += self.velocity

        def update(self):
            self.change_direction()
            self.apply_velocity()

    class Level_5_Poison(pygame.sprite.Sprite):

        def __init__(self, current, target):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, './level 5/images/projectiles/poison.png')), (80, 70))
            self.rect = self.image.get_rect(center=current)
            self.speed = 5
            self.target = target

            self.direction = self.get_direction()

        def get_direction(self):
            start = self.rect.center
            target = self.target
            dx, dy = target[0] - start[0], target[1] - start[1]
            distance = math.hypot(dx, dy)  # Distance between two points
            if distance == 0:  # Avoid division by zero
                return 0, 0
            return dx / distance, dy / distance  # Return normalized vector

        def apply_speed(self):
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

        def apply_death(self):
            top, bottom, left, right = self.rect.top, self.rect.bottom, self.rect.left, self.rect.right
            if top < 0 or left < 0:
                self.kill()
            elif bottom > HEIGHT or right > WIDTH:
                self.kill()

        def update(self):
            self.apply_speed()
            self.apply_death()

    class Level_5_Rama_Health_Bar(pygame.sprite.Sprite):

        hp = 5

        def __init__(self):
            super().__init__()
            self.images = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, f'./level 5/images/player/health/hp({i}).png')), (175, 30)) for i in range(0, 6)]
            pos = (400, 20)
            self.image = self.images[Level_5_Rama_Health_Bar.hp]
            self.rect = self.image.get_rect(topleft=pos)
            self.message_surf = font.render("Rama: ", False, 'white')
            self.message_rect = self.message_surf.get_rect(topleft=(325, 20))

        def update(self):
            screen.blit(self.message_surf, self.message_rect)
            self.image = self.images[Level_5_Rama_Health_Bar.hp]

    class Level_5_Indrajith_Health_Bar(pygame.sprite.Sprite):

        hp = 5

        def __init__(self):
            super().__init__()
            self.images = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, f'./level 5/images/enemy/health/hp({i}).png')), (175, 30)) for i in range(0, 6)]
            pos = (WIDTH - 300, 20)
            self.image = self.images[Level_5_Indrajith_Health_Bar.hp]
            self.rect = self.image.get_rect(topleft=pos)
            self.message_surf = font.render(" :Indrajith", False, 'white')
            self.message_rect = self.message_surf.get_rect(topleft=(WIDTH - 125, 20))

        def update(self):
            screen.blit(self.message_surf, self.message_rect)
            self.image = self.images[Level_5_Indrajith_Health_Bar.hp]

    # Level 6 classes ======================================================================================================

    class Level_6_Hanuman(pygame.sprite.Sprite):
        
        gravity = 1

        def __init__(self):
            super().__init__()
            self.player_fly = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, f'./level 6/images/player/hanuman_{i}.png')), (204, 80)) for i in range(1, 5)]
            self.player_index = 0
            self.upwards_flight_flag = False
            self.image = self.player_fly[self.player_index]
            self.rect = self.image.get_rect(topleft=(50, 400))
            self.rect = self.rect.inflate(-20, 0)

        def player_input(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.upwards_flight_flag:
                Level_6_Hanuman.gravity = -10
            self.upwards_flight_flag = keys[pygame.K_SPACE]

        def gravity_apply(self):
            self.rect.y += Level_6_Hanuman.gravity
            if Level_6_Hanuman.gravity < 3:
                Level_6_Hanuman.gravity += 1
            if self.rect.top > HEIGHT or self.rect.bottom < 0:
                self.kill()

        def animation_state(self):
            self.player_index += 0.125
            if self.player_index >= 4:
                self.player_index = 0
            self.image = self.player_fly[int(self.player_index)]

        def update(self):
            self.player_input()
            self.gravity_apply()
            self.animation_state()
            
    class Level_6_Obstacles(pygame.sprite.Sprite):
        
        def __init__(self):
            super().__init__()
            if random.randint(1, 3) > 1:
                num = random.randint(1, 2)
                y = random.randint(20, HEIGHT - 300)
                if num == 1:
                    size = (212, 136)
                else:
                    size = (209, 111)
                self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, f'./level 6/images/obstacles/cloud_{num}.png')), size)
                self.rect = self.image.get_rect(topleft=(WIDTH, y))
            else:
                num = random.randint(1, 2)
                if num == 1:
                    size = (286, 184)
                    mod = 8
                else:
                    size = (292, 143)
                    mod = 5
                self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, f'./level 6/images/obstacles/mountain_{num}.png')), size)
                self.rect = self.image.get_rect(bottomleft=(WIDTH, HEIGHT + mod))

        def apply_movement(self):
            self.rect.x -= 5
            if self.rect.right <= 0:
                self.kill()

        def update(self):
            self.apply_movement()

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX CLASS XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX END XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    def load_gif_frames(gif_path):
        # Open the GIF file
        gif = Image.open(gif_path)

        # Store the frames as a list of Pygame surfaces
        frames = []

        try:
            while True:
                frame = gif.copy().convert("RGBA")
                pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                frames.append(pygame_image)

                gif.seek(gif.tell() + 1)

        except EOFError:
            pass  # End of GIF

        return frames

    def play_audio(clip_path):
        nonlocal stop_threads
        pygame.mixer.music.load(clip_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if stop_threads:
                pygame.mixer.music.stop()
                break
        stop_threads = False

    def play_video(video, audio, screen):
        nonlocal stop_threads, clock

        audio_thread = threading.Thread(target=play_audio, args=(audio,))
        stop_video = False

        if len(audio) != 0:
            audio_thread.start()

        # Play the video frame by frame
        for frame in video.iter_frames(fps=video.fps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    stop_threads = True
                    stop_video = True

            if stop_video:
                break

            # Convert the frame to a Pygame surface
            frame_surface = pygame.image.fromstring(frame.tobytes(), video.size, "RGB")

            # Clear the screen
            screen.fill((0, 0, 0))

            # Blit the frame onto the screen
            screen.blit(frame_surface, ((1280 - video.size[0]) // 2, (720 - video.size[1]) // 2))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(video.fps)

        if len(audio) != 0:
            audio_thread.join()

    def screen_blit(screen, text, cords, color):
        surf = font.render(text, False, color)
        rect = surf.get_rect(center=cords)
        screen.blit(surf, rect)

    # Level 1 Functions ====================================================================================================
    def lvl_1_enemy_player_collision():
        return pygame.sprite.spritecollide(lvl_1_rama_group.sprite, lvl_1_enemy_group, False)

    def lvl_1_ring_player_collide():
        return pygame.sprite.spritecollide(lvl_1_rama_group.sprite, lvl_1_ring_group, False)

    def lvl_1_display_distance(screen):
        nonlocal lvl_1_start_time
        distance = int(pygame.time.get_ticks() / 1000 - lvl_1_start_time)  # there will be a start time instead of 0 here, change it later
        distance_surf = font.render(f'{distance}/100 Distance', False, (64, 64, 64))
        distance_rect = distance_surf.get_rect(center=(WIDTH / 2, 50))
        screen.blit(distance_surf, distance_rect)

    def lvl_1_display_rings_collected(screen):
        rings_surf = font.render(f"{lvl_1_rings_collected}/3 Rings", False,(64, 64, 64))  # change it such that number of rings collected are displayed
        rings_rect = rings_surf.get_rect(center=(WIDTH / 2, 75))
        screen.blit(rings_surf, rings_rect)

    def lvl_1_display_update_background(screen):
        for ind, rect in enumerate(lvl_1_background_images_rects):
            screen.blit(lvl_1_background_images[ind], rect)
            rect.x -= 5
            if rect.right == 0:
                rect.left = WIDTH

    def lvl_1_game_reset():
        nonlocal lvl_1_enemy_spawn_time, lvl_1_enemy_spawn_speed_change_time, lvl_1_ring_spawn, lvl_1_ring_spawn_places, lvl_1_ring_ind, lvl_1_rings_collected

        lvl_1_enemy_group.empty()
        lvl_1_rama_group.sprite.rect.topleft = (50, 475)
        Level_1_Rama.gravity = 0

        pygame.time.set_timer(lvl_1_enemy_spawn_timer, 0)
        pygame.time.set_timer(lvl_1_enemy_spawn_speed_change_timer, 0)
        Level_1_Enemy.enemy_speed = 9
        lvl_1_enemy_spawn_time = 1500
        lvl_1_enemy_spawn_speed_change_time = 10000

        lvl_1_ring_spawn = False

        Level_1_Ring.ring_speed = 9
        lvl_1_ring_spawn_places = [random.randint(11, 30), random.randint(31, 60), random.randint(61, 90)]
        lvl_1_ring_ind = 0
        lvl_1_rings_collected = 0

    # Level 2 Functions ====================================================================================================

    def lvl_2_render_text(screen, text_lines):
        rendered_lines = []
        for i, line in enumerate(text_lines):
            rendered_line = font.render(line, True, (255, 255, 255))  # White color
            rendered_lines.append(rendered_line)

        # Display the text on the screen
        line_spacing = 40  # Adjust the spacing between lines as needed
        for i, rendered_line in enumerate(rendered_lines):
            screen.blit(rendered_line, (50, 50 + i * line_spacing))

    # Level 3 Functions ====================================================================================================
    def lvl_3_probability(success_percentage):
        # Generate a random number between 0 and 1
        random_number = random.random()

        # Compare the random number with the success percentage
        if random_number < success_percentage:
            return True
        else:
            return False

    def lvl_3_fire_bar_display(screen):
        nonlocal lvl_3_fire_dmg
        message_surf = font.render(
            f"Heat Bar ({int(int(pygame.time.get_ticks() / 1000 - lvl_3_start_time + lvl_3_fire_dmg) / 10)}/3)",
            False, (64, 64, 64))
        message_rect = message_surf.get_rect(center=(100, 50))
        screen.blit(message_surf, message_rect)
        temporary_rect = lvl_3_fire_static_rect
        temporary_rect.center = (225, 50)
        for i in range(0, int(int(pygame.time.get_ticks() / 1000 - lvl_3_start_time + lvl_3_fire_dmg) / 10)):
            screen.blit(lvl_3_fire_static_img, temporary_rect)
            temporary_rect.centerx += 75
        if int(pygame.time.get_ticks() / 1000 - lvl_3_start_time + lvl_3_fire_dmg) / 10.0 >= 3.1:
            return True
        return False

    def lvl_3_reset_fire():
        nonlocal lvl_3_fire_dmg, lvl_3_fire_tick
        lvl_3_fire_tick = False
        lvl_3_fire_dmg = 0

    def lvl_3_render_text(screen, text_lines):
        rendered_lines = []
        for i, line in enumerate(text_lines):
            rendered_line = font.render(line, True, (255, 255, 255))  # White color
            rendered_lines.append(rendered_line)

        # Display the text on the screen
        line_spacing = 40  # Adjust the spacing between lines as needed
        for i, rendered_line in enumerate(rendered_lines):
            screen.blit(rendered_line, (50, 50 + i * line_spacing))

    def lvl_3_questions_generator(start, end, exclude=None):
        number = random.randint(start, end - 1)
        if exclude is None:
            return number
        elif number == exclude and number == end - 1:
            return number - 1
        elif number == exclude:
            return number + 1
        else:
            return number

    # Level 4 Functions ====================================================================================================

    def lvl_4_shuffled_deck():
        images = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_1.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_1.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_2.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_2.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_3.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_3.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_4.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_4.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_5.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_5.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_6.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_6.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_7.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_7.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_8.png')), (128, 64)).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/cards/card_8.png')), (128, 64)).convert_alpha(),
        ]
        final_list = []
        for i in range(0, 16):
            number = random.randint(0, 15 - i)
            final_list.append(images[number])
            images.remove(images[number])
        return final_list

    def lvl_4_compare_images(img1, img2):
        # Check if images have the same dimensions
        if img1.get_width() != img2.get_width() or img1.get_height() != img2.get_height():
            return False

        # Compare pixels
        for x in range(img1.get_width()):
            for y in range(img1.get_height()):
                if img1.get_at((x, y)) != img2.get_at((x, y)):
                    return False
        return True

    def lvl_4_blit_background(screen):
        screen.blit(lvl_4_upper_bg, lvl_4_upper_bg_rect)
        screen.blit(lvl_4_lower_bg, lvl_4_lower_bg_rect)
        for i in range(0, int((16 - len(lvl_4_card_sprites.sprites())) / 2)):
            screen.blit(lvl_4_rock_img, lvl_4_rock_img.get_rect(topleft=(250 + i * 65, 275)))

    # Level 5 Functions ====================================================================================================

    def lvl_5_rama_arrow_pickup():
        nonlocal lvl_5_rama_group, lvl_5_arrow_spawn_group
        collided_sprites = pygame.sprite.spritecollide(lvl_5_rama_group.sprite, lvl_5_arrow_spawn_group, False)
        if collided_sprites:
            for sprite in collided_sprites:
                sprite.kill()
            return True
        return False

    def lvl_5_indrajith_arrow_collide():
        nonlocal lvl_5_indrajith_group, lvl_5_arrow_shot_group
        collided_sprites = pygame.sprite.spritecollide(lvl_5_indrajith_group.sprite, lvl_5_arrow_shot_group, False)
        return_value = False
        if collided_sprites:
            for sprite in collided_sprites:
                if math.fabs(sprite.rect.top - lvl_5_indrajith_group.sprite.rect.bottom) <= 5:
                    return_value = True
                sprite.kill()
        return return_value

    def lvl_5_rama_poison_collide():
        nonlocal lvl_5_rama_group, lvl_5_poison_group
        collided_sprites = pygame.sprite.spritecollide(lvl_5_rama_group.sprite, lvl_5_poison_group, False)
        if collided_sprites:
            for sprite in collided_sprites:
                sprite.kill()
            return True
        return False

    # Level 6 Functions ====================================================================================================

    def lvl_6_hanuman_obstacle_collide():
        nonlocal lvl_6_hanuman_group, lvl_6_obstacle_group
        collided_sprites = pygame.sprite.spritecollide(lvl_6_hanuman_group.sprite, lvl_6_obstacle_group, False)
        if collided_sprites:
            for sprite in collided_sprites:
                sprite.kill()
            return True
        return False

    def lvl_6_display_distance(screen):
        nonlocal lvl_6_start_time
        distance = int(pygame.time.get_ticks() / 1000 - lvl_6_start_time)  # there will be a start time instead of 0 here, change it later
        distance_surf = font.render(f'{distance}/60 Distance', False, (64, 64, 64))
        distance_rect = distance_surf.get_rect(center=(WIDTH / 2, 50))
        screen.blit(distance_surf, distance_rect)
        return distance == 60

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX FUNCTION XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX END XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    lvl_1_video, lvl_2_video, lvl_3_video, lvl_4_video, lvl_5_video, lvl_6_video, end_video = False, False, False, False, True, True, False #TODO change to False for both when the video has been made and set as lvl_x_vid below
    stop_threads = False
    stars = 0
    # Level 1 Variables ====================================================================================================
    os.path.join(base_path, )

    character_intro_vid = mp.VideoFileClip(os.path.join(base_path, './level 1/videos/Character introduction.mp4'))
    character_intro_audio = os.path.join(base_path, './level 1/audio/Character introduction.mp3')

    lvl_1_vid = mp.VideoFileClip(os.path.join(base_path, './level 1/videos/video_1.mp4'))
    lvl_1_audio = os.path.join(base_path, './level 1/audio/video_1.mp3')

    lvl_2_vid = mp.VideoFileClip(os.path.join(base_path, './level 2/videos/video_2.mp4'))
    lvl_2_audio = os.path.join(base_path, './level 2/audio/video_2.mp3')

    lvl_3_vid = mp.VideoFileClip(os.path.join(base_path, './level 3/videos/video_3.mp4'))
    lvl_3_audio = os.path.join(base_path, './level 3/audio/video_3.mp3')

    lvl_4_vid = mp.VideoFileClip(os.path.join(base_path, './level 4/videos/video_4.mp4'))
    lvl_4_audio = ''

    lvl_5_vid = ''
    lvl_5_audio = ''

    lvl_6_vid = ''
    lvl_6_audio = ''

    end_vid = mp.VideoFileClip(os.path.join(base_path, './level end/videos/video_end.mp4'))
    end_audio = ''

    good_audio = [os.path.join(base_path, './audio/good_1.mp3'), os.path.join(base_path, './audio/good_2.mp3'), os.path.join(base_path, './audio/good_3.mp3'), os.path.join(base_path, './audio/good_4.mp3')]
    bad_audio = [os.path.join(base_path, './audio/bad_1.mp3'), os.path.join(base_path, './audio/bad_1.mp3')]

    lvl_1_instructions_img = pygame.image.load(os.path.join(base_path, './level 1/images/instructions.jpg')).convert_alpha()
    lvl_1_instructions_rect = lvl_1_instructions_img.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    # lvl_1_instructions_gif = load_gif_frames('./level 1/images/instructions.gif')

    # player, enemy and ring groups
    lvl_1_rama_group = pygame.sprite.GroupSingle()
    lvl_1_rama_group.add(Level_1_Rama())
    lvl_1_enemy_group = pygame.sprite.Group()
    lvl_1_ring_group = pygame.sprite.GroupSingle()

    # enemy spawn and speed timers
    lvl_1_enemy_spawn_time = 1500
    lvl_1_enemy_spawn_timer = pygame.USEREVENT + 1
    lvl_1_enemy_spawn_speed_change_time = 10000
    lvl_1_enemy_spawn_speed_change_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(lvl_1_enemy_spawn_timer, 0)
    pygame.time.set_timer(lvl_1_enemy_spawn_speed_change_timer, 0)

    lvl_1_start_time = 0

    # ring variables
    lvl_1_ring_spawn = False
    lvl_1_ring_spawn_places = [random.randint(11, 30), random.randint(31, 60), random.randint(61, 90)]
    lvl_1_ring_ind = 0
    lvl_1_rings_collected = 0

    # background image list
    lvl_1_background_images = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 1/images/background.png')), (1280, 720)),
                               pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 1/images/background.png')),
                               (1280, 720)),
                               True, False)]

    # background image rect list
    lvl_1_background_images_rects = [lvl_1_background_images[0].get_rect(), lvl_1_background_images[1].get_rect()]
    lvl_1_background_images_rects[1].x = WIDTH

    # Level 2 Variables ====================================================================================================

    lvl_2_wheel = Level_2_Wheel()
    lvl_2_arrow = Level_2_Arrow()
    lvl_2_bow = Level_2_Bow()

    lvl_2_score = 0
    lvl_2_bg_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 2/images/bg.jpeg')), (1280, 720))
    lvl_2_bg_rect = lvl_2_bg_img.get_rect()

    # Level 3 Variables ====================================================================================================

    Level_3_TILESIZE = 64

    Level_3_WORLD_MAP = [
        ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x",
         "x", "x", "x", "x", "x", "x", "x", "x", "x"],
        ["x", " ", " ", " ", "x", "x", " ", "x", " ", " ", " ", " ", "x", "x", " ", " ", "x", " ", " ", " ", "x", " ",
         " ", " ", " ", " ", "x", " ", " ", " ", "x"],
        ["x", "x", "x", " ", "x", "x", " ", "x", " ", "x", "x", " ", " ", " ", " ", " ", "x", " ", "x", " ", "x", " ",
         "x", "x", "x", " ", "x", " ", "x", " ", "x"],
        ["x", " ", " ", " ", " ", " ", " ", "x", " ", "x", "x", "x", "x", "x", "x", " ", "x", " ", "x", " ", " ", " ",
         "x", " ", " ", " ", "x", " ", "x", " ", "x"],
        ["x", "x", "x", "x", "x", " ", "x", "x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", "x", " ", "x", " ",
         "x", "x", "x", " ", "x", " ", "x", " ", "x"],
        ["x", " ", " ", " ", "x", " ", "x", "x", " ", "x", "x", "x", "x", " ", "x", "x", "x", " ", "x", " ", "x", " ",
         "x", " ", " ", " ", "x", " ", "x", " ", "x"],
        ["x", " ", "x", " ", "x", " ", "x", "x", " ", "x", " ", " ", "x", " ", " ", " ", "x", " ", "x", " ", " ", " ",
         "x", "x", "x", " ", "x", " ", "x", " ", "x"],
        ["x", " ", "x", " ", "x", " ", "x", "x", " ", "x", " ", "x", "x", " ", "x", "x", "x", " ", "x", " ", "x", " ",
         " ", " ", " ", "x", " ", "x", " ", " ", "x"],
        ["x", " ", "x", " ", "x", " ", " ", " ", " ", "x", " ", "x", " ", " ", " ", " ", "x", " ", "x", " ", "x", "x",
         "x", "x", " ", "x", " ", "x", " ", "x", "x"],
        ["x", " ", "x", " ", "x", "x", "x", "x", "x", "x", " ", "x", " ", "x", "x", " ", "x", " ", "x", " ", "x", " ",
         " ", " ", " ", " ", "x", " ", " ", " ", "x"],
        ["x", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", "x", "x", " ", " ", " ", " ", " ", " ", "x",
         "x", "x", "x", " ", "x", " ", " ", " ", "x"],
        ["x", "x", "x", "x", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", " ", "x",
         " ", " ", " ", " ", "x", "x", "x", " ", "x"],
        ["x", " ", " ", " ", " ", " ", " ", "x", " ", "x", " ", "x", " ", "x", "x", " ", " ", " ", " ", " ", " ", "x",
         " ", "x", "x", " ", "x", " ", "x", " ", "x"],
        ["x", "x", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", " ", "x",
         " ", "x", " ", " ", " ", " ", "x", " ", "x"],
        ["x", " ", " ", " ", " ", "x", " ", "x", " ", "x", " ", "x", " ", "x", "x", " ", " ", " ", " ", " ", " ", "x",
         " ", "x", " ", "x", " ", "x", "x", " ", "x"],
        ["x", " ", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", " ", "x",
         " ", "x", " ", "x", " ", " ", " ", " ", "x"],
        ["x", " ", "x", " ", " ", " ", " ", " ", " ", "x", " ", "x", " ", "x", "x", " ", " ", " ", " ", " ", " ", "x",
         " ", " ", " ", "x", "x", "x", "x", " ", "x"],
        ["x", " ", "x", " ", "x", "x", "x", "x", "x", "x", " ", "x", " ", "x", "x", " ", "x", "x", "x", "x", "x", "x",
         "x", "x", " ", " ", " ", " ", "x", " ", "x"],
        ["x", " ", "x", " ", " ", " ", " ", "x", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
         " ", "x", " ", "x", " ", " ", "x", " ", "x"],
        ["x", " ", "x", "x", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", "x", "x",
         " ", "x", " ", "x", " ", " ", "x", " ", "x"],
        ["x", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", "x", " ", "x", "x", " ", " ", " ", " ", " ", " ", " ",
         " ", "x", " ", "x", " ", " ", "x", " ", "x"],
        ["x", "x", "x", "x", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", " ", "x",
         "x", "x", " ", " ", " ", " ", "x", " ", "x"],
        ["x", " ", " ", " ", " ", " ", " ", " ", " ", "x", " ", "x", " ", "x", "x", " ", " ", " ", " ", " ", " ", " ",
         " ", " ", " ", "x", "x", "x", "x", " ", "x"],
        ["x", " ", "x", "x", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", " ", "x",
         "x", "x", " ", "x", " ", " ", " ", " ", "x"],
        ["x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", "x",
         " ", " ", " ", "x", " ", "x", "x", "x", "x"],
        ["x", "x", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", " ", "x",
         "x", "x", " ", "x", " ", "x", " ", " ", "x"],
        ["x", " ", " ", " ", " ", "x", " ", "x", " ", "x", " ", "x", " ", "x", "x", " ", " ", " ", " ", " ", " ", "x",
         " ", "x", " ", "x", " ", "x", " ", "x", "x"],
        ["x", " ", "x", "x", "x", "x", " ", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", "x", "x", "x", "x", "x",
         " ", "x", " ", "x", " ", "x", " ", "x", "x"],
        ["x", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
         " ", " ", " ", " ", " ", " ", " ", " ", "x"],
        ["x", " ", "x", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
         " ", " ", " ", " ", " ", " ", " ", "p", "x"],
        ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x",
         "x", "x", "x", "x", "x", "x", "x", "x", "x"]
    ]

    lvl_3_sita_probability_counter = 0
    for xInd, x in enumerate(Level_3_WORLD_MAP):
        for yInd, y in enumerate(x):
            if y == " " and lvl_3_probability(lvl_3_sita_probability_counter):
                Level_3_WORLD_MAP[xInd][yInd] = "s"
                lvl_3_sita_probability_counter = -1
                break
            lvl_3_sita_probability_counter += 0.001
        if lvl_3_sita_probability_counter == -1:
            break

    lvl_3_level = Level_3_Level()

    lvl_3_fire_static_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "level 3/images/flamestatic.png")),
                                                   (64, 64)).convert_alpha()
    lvl_3_fire_static_rect = lvl_3_fire_static_img.get_rect()
    lvl_3_start_time = 0
    lvl_3_fire_tick_start_time = 0
    lvl_3_fire_tick = False
    lvl_3_fire_dmg = 0

    lvl_3_question_check = False
    lvl_3_questions = [
        [
            "1. Who is considered the 'Adi Kavi', or the original poet, of the Ramayana?",
            "a) Vyasa",
            "b) Valmiki",
            "c) Tulsidas",
            "d) Kalidasa"
        ],
        [
            "2. In which kingdom is the Ramayana primarily set?",
            "a) Ayodhya",
            "b) Kishkindha",
            "c) Lanka",
            "d) Mithila"
        ],
        [
            "3. Which celestial being is the mother of Lord Rama?",
            "a) Anjana",
            "b) Kausalya",
            "c) Kaikeyi",
            "d) Sumitra"
        ],
        [
            "4. What is the name of the sage who curses Ravana, leading to his downfall?",
            "a) Vishwamitra",
            "b) Agastya",
            "c) Durvasa",
            "d) Narada"
        ],
        [
            "5. Who is the wife of Lord Rama's devoted brother, Lakshmana?",
            "a) Mandodari",
            "b) Tara",
            "c) Urmila",
            "d) Sita"
        ],
        [
            "6. What is the name of the magical golden deer that tempts Sita and leads to her abduction?",
            "a) Maricha",
            "b) Surpanakha",
            "c) Hanuman",
            "d) Shabari"
        ],
        [
            "7. Which powerful weapon does Lord Rama use to kill Ravana?",
            "a) Brahmastra",
            "b) Pashupatastra",
            "c) Sudarshana Chakra",
            "d) Brahmashira"
        ],
        [
            "8. Which monkey warrior was crowned as the king of Kishkindha after Vali's death?",
            "a) Sugriva",
            "b) Angada",
            "c) Nala",
            "d) Jambavan"
        ],
        [
            "9. Who disguised himself as a golden deer to entice Sita?",
            "a) Ravana",
            "b) Maricha",
            "c) Vali",
            "d) Sugriva"
        ],
        [
            "10. Which sage did Sita seek shelter with after being banished from Ayodhya?",
            "a) Valmiki",
            "b) Vishwamitra",
            "c) Agastya",
            "d) Janaka"
        ]
    ]

    lvl_3_answers = [pygame.K_b, pygame.K_a, pygame.K_b, pygame.K_d, pygame.K_c, pygame.K_a, pygame.K_b, pygame.K_a,
                     pygame.K_b, pygame.K_a]
    lvl_3_questions_selected = [-1, -1]
    lvl_3_questions_answered = [False, False]
    lvl_3_pressed = False

    # Level 4 Variables ====================================================================================================

    lvl_4_timer_start = pygame.time.get_ticks()
    lvl_4_timer_duration = 60000
    lvl_4_card_sprites = pygame.sprite.Group()
    lvl_4_mouse_clicked = False

    lvl_4_x_multiplier = 380
    lvl_4_y_multiplier = 80
    lvl_4_deck = []
    lvl_4_deck_iterable = 0

    lvl_4_cards_flipped_count = 0
    lvl_4_cards_flipped = []

    lvl_4_upper_bg = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/upper_bg.jpeg')),
                                            (1280, 360)).convert_alpha()
    lvl_4_upper_bg_rect = lvl_4_upper_bg.get_rect(topleft=(0, 0))
    lvl_4_lower_bg = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/lower_bg.png')),
                                            (1280, 360)).convert_alpha()
    lvl_4_lower_bg_rect = lvl_4_lower_bg.get_rect(topleft=(0, 360))
    lvl_4_rock_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'level 4/images/rock.png')), (64, 64)).convert_alpha()

    # Level 5 Variables ====================================================================================================

    lvl_5_rama_group = pygame.sprite.GroupSingle()
    lvl_5_rama_group.add(Level_5_Rama())

    lvl_5_arrow_spawn_group = pygame.sprite.Group()
    lvl_5_arrow_spawn_group.add(Level_5_Arrow_Spawn())

    lvl_5_indrajith_group = pygame.sprite.GroupSingle()
    lvl_5_indrajith_group.add(Level_5_Indrajith())

    lvl_5_arrow_shot_group = pygame.sprite.Group()

    lvl_5_poison_group = pygame.sprite.Group()

    lvl_5_rama_health_bar_group = pygame.sprite.GroupSingle()
    lvl_5_rama_health_bar_group.add(Level_5_Rama_Health_Bar())

    lvl_5_indrajith_health_bar_group = pygame.sprite.GroupSingle()
    lvl_5_indrajith_health_bar_group.add(Level_5_Indrajith_Health_Bar())

    lvl_5_arrow_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(lvl_5_arrow_spawn_event, 0)

    lvl_5_poison_shoot_event = pygame.USEREVENT + 2
    pygame.time.set_timer(lvl_5_poison_shoot_event, 0)

    lvl_5_arrow_shot_flag = False

    lvl_5_arrow_count_message_surf = font.render(f"Arrows: ({Level_5_Rama.arrows}/5)", False, "white")
    lvl_5_arrow_count_message_rect = lvl_5_arrow_count_message_surf.get_rect(topleft=(20, 20))

    lvl_5_bg_surf = pygame.transform.scale(pygame.image.load(os.path.join(base_path, './level 5/images/bg.jpg')), (1280, 720))
    lvl_5_bg_rect = lvl_5_bg_surf.get_rect(topleft=(0, 0))

    # Level 6 Variables ====================================================================================================

    lvl_6_hanuman_group = pygame.sprite.GroupSingle()
    lvl_6_hanuman_group.add(Level_6_Hanuman())

    lvl_6_obstacle_group = pygame.sprite.Group()

    lvl_6_obstacle_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(lvl_6_obstacle_spawn_event, 0)

    lvl_6_start_time = 0

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX VARIABLES XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX END XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Game loop starts
    while True:
        if not game_state and intro and game_level == 1:
            # set the starting screen with a dead eagle and rama
            if not lvl_1_video:
                play_video(character_intro_vid, character_intro_audio, screen)
                play_video(lvl_1_vid, lvl_1_audio, screen)
                lvl_1_video = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    intro = False
                    pygame.time.set_timer(lvl_1_enemy_spawn_timer, lvl_1_enemy_spawn_time)
                    pygame.time.set_timer(lvl_1_enemy_spawn_speed_change_timer, lvl_1_enemy_spawn_speed_change_time)
                    lvl_1_start_time = pygame.time.get_ticks() / 1000

            screen.fill("black")
            # screen.blit(message_surf, message_rect)
            screen.blit(lvl_1_instructions_img, lvl_1_instructions_rect)

        elif game_state and game_level == 1:
            # do stuff for game level 1
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if event.type == lvl_1_enemy_spawn_timer:
                    if not lvl_1_ring_spawn:
                        lvl_1_enemy_group.add(Level_1_Enemy(None))
                    else:
                        lvl_1_ring_spawn = False
                        lvl_1_ring_group.add(Level_1_Ring(lvl_1_ring_ind + 1))
                        lvl_1_ring_ind += 1
                if event.type == lvl_1_enemy_spawn_speed_change_timer:
                    Level_1_Enemy.enemy_speed += 1
                    Level_1_Ring.ring_speed += 1
                    lvl_1_enemy_spawn_time -= 100

            lvl_1_display_update_background(screen)

            lvl_1_rama_group.draw(screen)
            lvl_1_rama_group.update(lvl_1_enemy_group)

            lvl_1_enemy_group.draw(screen)
            lvl_1_enemy_group.update()

            lvl_1_ring_group.draw(screen)
            lvl_1_ring_group.update()

            lvl_1_display_distance(screen)
            lvl_1_display_rings_collected(screen)

            if lvl_1_enemy_player_collision():
                pygame.mixer.music.load(bad_audio[random.randint(0, 1)])
                pygame.mixer.music.play()
                game_state = False
                lvl_1_game_reset()

            if lvl_1_ring_player_collide():
                pygame.mixer.music.load(good_audio[random.randint(0, 3)])
                pygame.mixer.music.play()
                lvl_1_rings_collected += 1
                lvl_1_ring_group.empty()

            if lvl_1_ring_ind < 3 and int(pygame.time.get_ticks() / 1000 - lvl_1_start_time) >= lvl_1_ring_spawn_places[lvl_1_ring_ind]:
                lvl_1_ring_spawn = True

            if int(pygame.time.get_ticks() / 1000 - lvl_1_start_time) >= 100:
                game_state = False
                if lvl_1_rings_collected == 3:
                    intro = True
                    game_level += 1
                    stars += 1
                lvl_1_game_reset()

        elif not game_state and not intro and game_level == 1:
            # do stuff for game level 1 dead
            Level_1_Rama.distances = 0
            Level_1_Rama.jumps = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()

                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    intro = False
                    pygame.time.set_timer(lvl_1_enemy_spawn_timer, lvl_1_enemy_spawn_time)
                    pygame.time.set_timer(lvl_1_enemy_spawn_speed_change_timer, lvl_1_enemy_spawn_speed_change_time)
                    lvl_1_start_time = pygame.time.get_ticks() / 1000

            screen.fill("black")
            message_surf = font.render(f"LVL 1\nYou died!\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif not game_state and intro and game_level == 2:
            # set the starting screen for game level 2
            if not lvl_2_video:
                play_video(lvl_2_vid, lvl_2_audio, screen)
                lvl_2_video = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    intro = False

            screen.fill("black")
            message_surf = font.render(f"LVL 2\nSample text.\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif game_state and game_level == 2:
            # do stuff for game level 2
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                pass
            screen.blit(lvl_2_bg_img, lvl_2_bg_rect)

            screen.blit(lvl_2_wheel.image, lvl_2_wheel.rect)
            lvl_2_wheel.update()
            screen.blit(lvl_2_arrow.image, lvl_2_arrow.rect)
            lvl_2_arrow.update()
            if game_state:
                screen.blit(lvl_2_bow.image, lvl_2_bow.rect)
                lvl_2_bow.update()
                lvl_2_render_text(screen, [f"Score: {lvl_2_score}/3", "Hit the orange sector"])
                if lvl_2_score == 3:
                    game_state = False
                    intro = True
                    game_level += 1
                    stars += 1
            else:
                lvl_2_score = 0
                lvl_2_arrow.kill()
                lvl_2_wheel.kill()
                lvl_2_bow.kill()

        elif not game_state and not intro and game_level == 2:
            # do stuff for game level 2 dead
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    lvl_2_arrow = Level_2_Arrow()
                    lvl_2_wheel = Level_2_Wheel()
                    lvl_2_bow = Level_2_Bow()

            screen.fill("black")
            message_surf = font.render(f"LVL 2\nYou died!\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif not game_state and intro and game_level == 3:
            # set the starting screen for game level 3
            if not lvl_3_video:
                lvl_3_video = True
                play_video(lvl_3_vid, lvl_3_audio, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    intro = False
                    lvl_3_start_time = pygame.time.get_ticks() / 1000

            screen.fill("black")
            message_surf = font.render(f"LVL 3\nSample text.\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif game_state and game_level == 3:
            # do stuff for game level 3
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()
                if not keys[pygame.K_a] and not keys[pygame.K_b] and not keys[pygame.K_c] and not keys[pygame.K_d]:
                    lvl_3_pressed = False
                if lvl_3_question_check and not lvl_3_questions_answered[0] and not lvl_3_pressed:
                    if keys[lvl_3_answers[lvl_3_questions_selected[0]]]:
                        lvl_3_questions_answered[0] = True
                        lvl_3_pressed = True
                    elif keys[pygame.K_a] or keys[pygame.K_b] or keys[pygame.K_c] or keys[pygame.K_d]:
                        pygame.mixer.music.load(bad_audio[random.randint(0, 1)])
                        pygame.mixer.music.play()
                        game_state = False
                        lvl_3_pressed = True
                        lvl_3_question_check = False
                elif lvl_3_question_check and not lvl_3_questions_answered[1] and not lvl_3_pressed:
                    if keys[lvl_3_answers[lvl_3_questions_selected[1]]]:
                        lvl_3_questions_answered[1] = True
                        lvl_3_pressed = True
                    elif keys[pygame.K_a] or keys[pygame.K_b] or keys[pygame.K_c] or keys[pygame.K_d]:
                        pygame.mixer.music.load(bad_audio[random.randint(0, 1)])
                        pygame.mixer.music.play()
                        game_state = False
                        lvl_3_pressed = True
                        lvl_3_question_check = False

            if lvl_3_question_check:
                if not lvl_3_questions_answered[0]:
                    lvl_3_render_text(screen, lvl_3_questions[lvl_3_questions_selected[0]])
                    pygame.mixer.music.load(good_audio[random.randint(0, 3)])
                    pygame.mixer.music.play()
                elif not lvl_3_questions_answered[1]:
                    lvl_3_render_text(screen, lvl_3_questions[lvl_3_questions_selected[1]])
                else:
                    game_state = False
                    intro = True
                    game_level += 1
                    stars += 1
            else:
                lvl_3_level.run()
                if lvl_3_fire_bar_display(screen):
                    game_state = False
                    lvl_3_level.game_end()
                    lvl_3_level = Level_3_Level()
                    lvl_3_reset_fire()

                if lvl_3_level.player_sita_collide() and game_state:
                    pygame.mixer.music.load(good_audio[random.randint(0, 3)])
                    pygame.mixer.music.play()
                    lvl_3_questions_answered = [False, False]
                    lvl_3_questions_selected[0] = lvl_3_questions_generator(0, 10)
                    lvl_3_questions_selected[1] = lvl_3_questions_generator(0, 10, lvl_3_questions_selected[0])
                    lvl_3_question_check = True
                    lvl_3_level.game_end()
                    lvl_3_reset_fire()

        elif not game_state and not intro and game_level == 3:
            # do stuff for game level 3 dead
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    lvl_3_level = Level_3_Level()
                    lvl_3_start_time = pygame.time.get_ticks() / 1000

            screen.fill("black")
            message_surf = font.render(f"LVL 3\nYou died!\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif not game_state and intro and game_level == 4:
            # set the starting screen for game level 4
            if not lvl_4_video:
                lvl_4_video = True
                play_video(lvl_4_vid, lvl_4_audio, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    intro = False
                    lvl_4_timer_start = pygame.time.get_ticks()

                    lvl_4_deck = lvl_4_shuffled_deck()
                    for i in range(0, 4):
                        for j in range(0, 4):
                            lvl_4_card_sprites.add(Level_4_Cards(lvl_4_deck[lvl_4_deck_iterable], (0 + i * lvl_4_x_multiplier, 370 + j * lvl_4_y_multiplier)))
                            lvl_4_deck_iterable += 1

            screen.fill("black")
            message_surf = font.render(f"LVL 4\nSample text.\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif game_state and game_level == 4:
            # do stuff for game level 4
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
            screen.fill('grey')
            lvl_4_blit_background(screen)

            if len(lvl_4_card_sprites.sprites()) == 0:
                lvl_4_blit_background(screen)
                lvl_4_card_sprites.draw(screen)
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)
                game_state = False
                intro = True
                game_level += 1
                stars += 1

            lvl_4_card_sprites.draw(screen)
            lvl_4_card_sprites.update()

            lvl_4_elapsed_time = pygame.time.get_ticks() - lvl_4_timer_start
            lvl_4_remaining_time = max(0, (lvl_4_timer_duration - lvl_4_elapsed_time) // 1000)

            if lvl_4_remaining_time == 0:
                game_state = False

            message_surf = font.render(f"Time: {lvl_4_remaining_time}", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, 100))
            screen.blit(message_surf, message_rect)

            if lvl_4_cards_flipped_count == 2:
                screen.fill('grey')
                lvl_4_blit_background(screen)
                lvl_4_card_sprites.draw(screen)
                screen.blit(message_surf, message_rect)
                pygame.display.update()
                clock.tick(60)
                pygame.time.wait(1000)

                if lvl_4_compare_images(lvl_4_cards_flipped[0].image_list[1], lvl_4_cards_flipped[1].image_list[1]):
                    lvl_4_cards_flipped[0].kill()
                    lvl_4_cards_flipped[1].kill()
                    lvl_4_cards_flipped.clear()
                    lvl_4_cards_flipped_count = 0
                    if len(lvl_4_card_sprites.sprites()) != 0:
                        pygame.mixer.music.load(good_audio[random.randint(0, 3)])
                        pygame.mixer.music.play()
                else:
                    lvl_4_cards_flipped[0].swap_state()
                    lvl_4_cards_flipped[1].swap_state()
                    lvl_4_cards_flipped.clear()
                    lvl_4_cards_flipped_count = 0

        elif not game_state and not intro and game_level == 4:
            # do stuff for game level 4 dead
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    lvl_4_timer_start = pygame.time.get_ticks()
                    lvl_4_deck = lvl_4_shuffled_deck()
                    lvl_4_deck_iterable = 0
                    lvl_4_card_sprites.empty()
                    for i in range(0, 4):
                        for j in range(0, 4):
                            lvl_4_card_sprites.add(Level_4_Cards(lvl_4_deck[lvl_4_deck_iterable], (0 + i * lvl_4_x_multiplier, 370 + j * lvl_4_y_multiplier)))
                            lvl_4_deck_iterable += 1

            screen.fill("black")
            message_surf = font.render(f"LVL 4\nYou died!\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif not game_state and intro and game_level == 5:
            # set the starting screen for game level 5
            if not lvl_5_video:
                lvl_5_video = True
                play_video(lvl_5_vid, lvl_5_audio, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    intro = False
                    pygame.time.set_timer(lvl_5_poison_shoot_event, 2500)

            screen.fill("black")
            message_surf = font.render(f"LVL 5\nSample text.\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif game_state and not intro and game_level == 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == lvl_5_arrow_spawn_event:
                    pygame.time.set_timer(lvl_5_arrow_spawn_event, 0)
                    lvl_5_arrow_spawn_group.add(Level_5_Arrow_Spawn())
                if event.type == lvl_5_poison_shoot_event:
                    lvl_5_poison_group.add(Level_5_Poison(lvl_5_indrajith_group.sprite.rect.midbottom, lvl_5_rama_group.sprite.rect.center))
                if pygame.key.get_pressed()[pygame.K_SPACE] and not lvl_5_arrow_shot_flag and Level_5_Rama.arrows > 0:
                    lvl_5_arrow_shot_group.add(Level_5_Arrow_Shot(lvl_5_rama_group.sprite.rect.midtop, pygame.mouse.get_pos()))
                    Level_5_Rama.arrows -= 1
                lvl_5_arrow_shot_flag = pygame.key.get_pressed()[pygame.K_SPACE]

            screen.fill((0, 0, 0))

            screen.blit(lvl_5_bg_surf, lvl_5_bg_rect)

            lvl_5_arrow_spawn_group.draw(screen)

            lvl_5_arrow_shot_group.draw(screen)
            lvl_5_arrow_shot_group.update()

            lvl_5_poison_group.draw(screen)
            lvl_5_poison_group.update()

            pygame.sprite.groupcollide(lvl_5_arrow_shot_group, lvl_5_poison_group, True, True)

            lvl_5_indrajith_group.draw(screen)
            lvl_5_indrajith_group.update()

            lvl_5_rama_group.draw(screen)
            lvl_5_rama_group.update()

            lvl_5_rama_health_bar_group.draw(screen)
            lvl_5_rama_health_bar_group.update()

            lvl_5_indrajith_health_bar_group.draw(screen)
            lvl_5_indrajith_health_bar_group.update()

            if lvl_5_rama_arrow_pickup():
                pygame.time.set_timer(lvl_5_arrow_spawn_event, 5000)
                if Level_5_Rama.arrows < 5:
                    Level_5_Rama.arrows += 1

            if lvl_5_indrajith_arrow_collide():
                if Level_5_Indrajith_Health_Bar.hp > 1:
                    Level_5_Indrajith_Health_Bar.hp -= 1
                else:
                    lvl_5_rama_group.empty()
                    lvl_5_indrajith_group.empty()
                    lvl_5_arrow_spawn_group.empty()
                    lvl_5_arrow_shot_group.empty()
                    lvl_5_poison_group.empty()

                    pygame.time.set_timer(lvl_5_arrow_spawn_event, 0)
                    pygame.time.set_timer(lvl_5_poison_shoot_event, 0)

                    game_state = False
                    intro = True
                    game_level += 1

            if game_state:

                # Proceed with the rest of the code only if the game has not stopped

                if lvl_5_rama_poison_collide():
                    if Level_5_Rama_Health_Bar.hp > 1:
                        Level_5_Rama_Health_Bar.hp -= 1
                    else:
                        lvl_5_rama_group.empty()
                        lvl_5_indrajith_group.empty()
                        lvl_5_arrow_spawn_group.empty()
                        lvl_5_arrow_shot_group.empty()
                        lvl_5_poison_group.empty()

                        Level_5_Rama_Health_Bar.hp = 5
                        Level_5_Indrajith_Health_Bar.hp = 5
                        Level_5_Rama.arrows = 0

                        lvl_5_rama_group.add(Level_5_Rama())
                        lvl_5_indrajith_group.add(Level_5_Indrajith())
                        lvl_5_arrow_spawn_group.add(Level_5_Arrow_Spawn())

                        pygame.time.set_timer(lvl_5_arrow_spawn_event, 0)
                        pygame.time.set_timer(lvl_5_poison_shoot_event, 0)

                        game_state = False

                lvl_5_arrow_count_message_surf = font.render(f"Arrows: ({Level_5_Rama.arrows}/5)", False, 'white')
                screen.blit(lvl_5_arrow_count_message_surf, lvl_5_arrow_count_message_rect)

        elif not game_state and not intro and game_level == 5:
            # do stuff for game level 5 dead
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    game_state = True
                    pygame.time.set_timer(lvl_5_poison_shoot_event, 2500)

            screen.fill("black")
            message_surf = font.render(f"LVL 5\nYou died!\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif not game_state and intro and game_level == 6:
            # set the starting screen for game level 6
            if not lvl_6_video:
                lvl_6_video = True
                play_video(lvl_6_vid, lvl_6_audio, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    lvl_6_start_time = pygame.time.get_ticks() / 1000
                    game_state = True
                    intro = False
                    pygame.time.set_timer(lvl_6_obstacle_spawn_event, 2000)

            screen.fill("black")
            message_surf = font.render(f"LVL 6\nSample text.\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        elif game_state and game_level == 6:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == lvl_6_obstacle_spawn_event:
                    lvl_6_obstacle_group.add(Level_6_Obstacles())

            screen.fill((0, 0, 200))

            lvl_6_hanuman_group.draw(screen)
            lvl_6_hanuman_group.update()

            lvl_6_obstacle_group.draw(screen)
            lvl_6_obstacle_group.update()

            if len(lvl_6_hanuman_group.sprites()) == 0:
                stop_threads = True
                game_state = False
                Level_6_Hanuman.gravity = 1
                lvl_6_obstacle_group.empty()

            if game_state and lvl_6_hanuman_obstacle_collide():
                stop_threads = True
                game_state = False
                lvl_6_obstacle_group.empty()
                Level_6_Hanuman.gravity = 1

            if game_state and lvl_6_display_distance(screen):
                lvl_6_obstacle_group.empty()
                stop_threads = True
                game_state = False
                game_level += 1

        elif not game_state and not intro and game_level == 6:
            # do stuff for game level 6 dead
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    lvl_6_start_time = pygame.time.get_ticks() / 1000
                    game_state = True
                    lvl_6_hanuman_group.add(Level_6_Hanuman())

            screen.fill("black")
            message_surf = font.render(f"LVL 6\nYou died!\nPress Enter to start.\n", False, "white")
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        else:
            # game over!
            if not end_video:
                play_video(end_vid, end_audio, screen)
                end_video = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    sys.exit()
            screen.fill('black')
            message = f"Story written by Valmiki\n"
            if Level_1_Rama.distances != 0:
                message += f"Average Jump Distance: {Level_1_Rama.distances / Level_1_Rama.jumps}"
            message_surf = font.render(message, None, 'white')
            message_rect = message_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(message_surf, message_rect)

        pygame.display.update()
        clock.tick(60)


#__main__()
