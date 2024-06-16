import os

import pygame
import pickle
from os import path
import random
import webbrowser


pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 900
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("we do a little gaming")

#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 40)

#define game variables
tile_size = 50
game_over = 0
main_menu = True
score = 0
level = 1
max_levels = 3
list1 = [1, -1]
list2 = [4, -4]
jump = pygame.mixer.Sound('untitled.wav')
eat = pygame.mixer.Sound('eat.wav')
level_done = pygame.mixer.Sound('level_done.wav')
losing_sound = pygame.mixer.Sound('losing_sound.wav')

#define color
white = (255, 255, 255)
blue = (0, 0, 255)
#load images

bg_img = pygame.image.load("sky.png")
resa = pygame.image.load("restart_btn.png")
restart_img = pygame.transform.scale(resa,(300,175))
stards =  pygame.image.load("start_btn.png")
start_img = pygame.transform.scale(stards,(300,175))
esaxsa = pygame.image.load("exit_btn.png")
exit_img = pygame.transform.scale(esaxsa,(300,175))
sign = pygame.image.load("sign.png")
sign2 = pygame.transform.scale(sign,(700,1400))

#draw grid for backgrounds

def draw_grid():
    for line in range(0, 36):
        pygame.draw.line(screen, (255, 255, 255), (0,line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0),(line * tile_size, screen_height))
        pygame.draw.rect(screen, (255, 255, 255), player.rect, 2)



def draw_text (text, font,  text_col, x , y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    opposum_group.empty()
    platform_group.empty()
    coin_group.empty()
    deathcoin_group.empty()
    # load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world




class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse posiition
        pos = pygame.mouse.get_pos()

        #check mouse over and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)
        return action

class Player():
   def __init__(self, x, y):
       self.reset( x, y)

   def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 10
        col_thresh = 20

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
               self.vel_y = -15
               self.jumped = True
               jump.play()
            if key[pygame.K_SPACE] == False :
               self.jumped = False
            if key[pygame.K_a]:
               dx -= 3
               self.counter += 1
               self.direction = -1
            if key[pygame.K_d]:
               dx += 3
               self.counter += 1
               self.direction = 1
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
               self.counter = 0
               self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]


            #handle  animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                     self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                #check or collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                        self.in_air = True
                    # check if below the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False



            #check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, opposum_group, False):
                game_over = -1
            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            #check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
            if pygame.sprite.spritecollide(self, deathcoin_group, False):
                game_over = -1

            #check for collision with platform
            for platform in platform_group:
                #collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below  platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    #move sideways with the platform
                    if  platform.move_x != 0:
                        self.rect.x += platform.move_direction

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('YOU  DIED!', font, blue, (screen_width // 1.7) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        #draw player onto screen
        screen.blit(self.image, self.rect)


        return game_over

   def reset(self, x, y):
       self.images_right = []
       self.images_left = []
       self.index = 0
       self.counter = 0
       for num in range(1, 5):
           img_right = pygame.image.load(f"guy{num}.png")
           img_right = pygame.transform.scale(img_right, (45, 33))
           img_left = pygame.transform.flip(img_right, True, False)
           self.images_right.append(img_right)
           self.images_left.append(img_left)
       self.dead_image = pygame.image.load("ghost.png")
       self.image = self.images_right[self.index]
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.width = self.image.get_width()
       self.height = self.image.get_height()
       self.vel_y = 0
       self.jumped = False
       self.direction = 0
       self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load("dirt.png")
        stone_img = pygame.image.load("stone.png")
        grass_img = pygame.image.load("grass.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img , img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size //2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 9:
                    deathcoin = DeathCoin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    deathcoin_group.add(deathcoin)
                if tile == 10:
                    opposum = Enemy2(col_count * tile_size, row_count * tile_size + (tile_size // 2 + 6))
                    opposum_group.add(opposum)
                if tile == 11:
                    img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img , img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("blob.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = random.choice(list1)
        self.move_counter = 0


    def update(self):
        if pygame.key.get_pressed()[pygame.K_h]:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

        if self.move_direction == 1:
            self.image = pygame.image.load("blob.png")
        if self.move_direction == -1:
            self.image = pygame.image.load("blobflipped.png")
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("opposumflipped.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = random.choice(list2)
        self.move_counter = 0

    def update(self):
        if pygame.key.get_pressed()[pygame.K_h]:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1

        if self.move_direction == 4:
            self.image = pygame.image.load("opposumflipped.png")
        if self.move_direction == -4:
            self.image = pygame.image.load("opposum.png")
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("lava.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
class DeathCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("meat.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
deathcoin_group = pygame.sprite.Group()
opposum_group = pygame.sprite.Group()


#create dummy coin for chowing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world\
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

#buttons
restart_button = Button(screen_width // 2 - 350, screen_height // 1.5,  restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 1.5,  start_img)
exit_button = Button(screen_width // 2 + 50, screen_height // 1.5,  exit_img)

run = True
while run:

    clock.tick(fps)

    screen. blit(bg_img, (0, 0))




    if main_menu == True:
        screen.blit(sign2, (100,-370))
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    else:
        world.draw()

        if game_over == 0:
             blob_group.update()
             platform_group.update()
             opposum_group.update()

             #update score
             #check if a coin has been collected
             if pygame.sprite.spritecollide(player,  coin_group, True):
                score += 1
                eat.play()
             if pygame.sprite.spritecollide(player, deathcoin_group, True):
                 game_over = -1
             draw_text('X ' + str(score) + '/10', font_score, white, tile_size - 10, 4)

        blob_group.draw(screen)
        lava_group.draw(screen)
        platform_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)
        deathcoin_group.draw(screen)
        opposum_group.draw(screen)
        game_over = player.update(game_over)

        if pygame.key.get_pressed()[pygame.K_h]:
             draw_grid()

        if pygame.key.get_pressed()[pygame.K_0]:
            webbrowser.open(r"https://forms.gle/91uxK71iz3VmFmdM7")
        #if player died
        if game_over == -1:
            losing_sound.play()
            if restart_button.draw():
                player.reset(100, screen_height - 130)
                blob_group.empty()
                lava_group.empty()
                exit_group.empty()
                platform_group.empty()
                opposum_group.empty()
                level = 1
                world = reset_level(level)
                game_over = 0
                score = 0
                coin_group.add(score_coin)
            else:
                if restart_button.draw():
                    blob_group.empty()
                    lava_group.empty()
                    exit_group.empty()
                    platform_group.empty()
                    opposum_group.empty()
                    world = reset_level(level)
                    score = 0
                    coin_group.add(score_coin)
            if exit_button.draw():
                run = False
        #if player has completed the level
        if game_over == 1 and score == 10:
            level += 1
            if level <= max_levels:
                #draw_text("Nice You Completed The Level!", font, blue, (screen_width // 2) - 140, screen_height // 2)
                world_data = []
                world = reset_level(level)
                score = 0
                game_over = 0
                coin_group.add(score_coin)
                level_done.play()
            else:
                pass
            if exit_button.draw():
                run = False
        elif game_over == 1 and score < 10:
            draw_text("You Died Of Starvation!", font, blue, (screen_width // 2) - 140, screen_height // 2)
            losing_sound.play()
            if exit_button.draw():
                run = False



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()