import pygame, math, sys
import csv
from character import Character
import Constants 
from weapon import Weapon
from world import World


pygame.init()

screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
pygame.display.set_caption("6.S sommatif")

#create clock for maintaining frame rate
clock = pygame.time.Clock()

#define game variables
level = 1
screen_scroll = [0, 0]

#define player movement variable
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#font
font = pygame.font.Font("fonts/comic-sans-ms/COMIC.TTF", 20)
#player image

#Helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

#battery images

life_full = scale_img(pygame.image.load("items/life/life.png").convert_alpha(), Constants.ITEM_SCALE)
life_half = scale_img(pygame.image.load("items/life/life_half.png").convert_alpha(), Constants.ITEM_SCALE)
life_empty = scale_img(pygame.image.load("items/life/life_empty.png").convert_alpha(), Constants.ITEM_SCALE)


#battery pickup
battery = scale_img(pygame.image.load("items/battery/0.png").convert_alpha(), Constants.ITEM_SCALE) 

#load weapon images
weapon_image = scale_img(pygame.image.load("weapons/pistol/0.png").convert_alpha(), Constants.WEAPON_SCALE)
bullet_image = scale_img(pygame.image.load("weapons/bullet.png").convert_alpha(), Constants.WEAPON_SCALE)

#load tile map images
tile_list = []
for x in range(Constants.TILE_TYPES):
    tile_image = pygame.image.load(f"tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (Constants.TILE_SIZE, Constants.TILE_SIZE))
    tile_list.append(tile_image)

#load chracter images   
mob_animations = []
mob_types = ["Player",  "R.O.B", "Long_arms", "Drone"]

animation_types = ["idle", "run"]
for mob in mob_types:
    #load images
    animation_list = []
    for animation in animation_types:
        #reset temp list of images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, Constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)


#function top ui
def draw_info():
    pygame.draw.rect(screen, Constants.pannel, (0, 0, Constants.SCREEN_WIDTH, 60))
    pygame.draw.line(screen, Constants.white, (0, 60), (Constants.SCREEN_WIDTH, 60))
    #lives
    half_life_drawn = False
    for i in range (5):
        if player.health >= ((i + 1) * 20):
            screen.blit(life_full, (10 + i * 30, -5))
        elif (player.health % 20 > 0) and half_life_drawn == False:
            screen.blit(life_half, (10 + i * 30, -5))
            half_life_drawn = True
        else:
           screen.blit(life_empty, (10 + i * 30, -5))


#create empty tile list
world_data = []
for rown in range(Constants.ROWS):  
    r = [-1] * Constants.COLS
    world_data.append(r)
#load lvl data
with open(f"levels/lvl_{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter= ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


world = World()
world.process_data(world_data, tile_list, mob_animations)



#damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        #screen_scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

#Create player
player = Character(400, 400, 100, mob_animations, 0)
#create player weapons
weapon = Weapon(weapon_image, bullet_image)
#empty enemy list
enemy_list = world.character_list



#create sprite groups
damage_text_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()



#Main loop
run = True
while run:

    #ctrl fps
    clock.tick(Constants.fps)

    screen.fill(Constants.bg)

    

    #calculate player movement
    dx = 0
    dy = 0
    if moving_right == True:
        dx = Constants.speed
    if moving_left == True:
        dx = -Constants.speed
    if moving_up == True:
        dy = -Constants.speed
    if moving_down == True:
        dy = Constants.speed

    #move player
    screen_scroll = player.move(dx, dy, world.obstacle_tiles)

    #update all objects
    world.update(screen_scroll)
    for enemy in enemy_list:
        enemy.ai(player, world.obstacle_tiles, screen_scroll)
        if enemy.alive:
            enemy.update()
    player.update()
    bullet = weapon.update(player)
    if bullet:
        bullet_group.add(bullet)
    for bullet in bullet_group:
        damage, damage_pos = bullet.update(screen_scroll, world.obstacle_tiles, enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), Constants.red)
            damage_text_group.add(damage_text)
    damage_text_group.update()


    
    #draw player on screen
    world.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    weapon.draw(screen)
    for bullet in bullet_group:
        bullet.draw(screen)
    damage_text_group.draw(screen)
    draw_info()
    
    


    world = World()
    world.process_data(world_data, tile_list, mob_animations)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            

        #keyboard pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

            

    pygame.display.update()
    

    
pygame.quit()