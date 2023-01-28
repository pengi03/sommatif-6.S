import pygame, sys
import Constants
import math


class Character():
    def __init__(self, x, y, health, mob_animations, char_type):
        self.char_type = char_type
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0 #0 = idle, 1 = run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.stunlock = False

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, Constants.TILE_SIZE, Constants.TILE_SIZE)
        self.rect.center = (x, y)
        

    def move(self, dx, dy, obstacle_tiles):
        screen_scroll = [0, 0]
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        #diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)


        self.rect.x += dx
    
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        self.rect.y += dy

        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom


        if self.char_type == 0:
            #hit door?
            #camera l / r
            if self.rect.right > (Constants.SCREEN_WIDTH - Constants.SCROLL_THRESH):
                screen_scroll[0] = (Constants.SCREEN_WIDTH - Constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = Constants.SCREEN_WIDTH - Constants.SCROLL_THRESH
            if self.rect.left < Constants.SCROLL_THRESH:
                screen_scroll[0] = Constants.SCROLL_THRESH - self.rect.left
                self.rect.left = Constants.SCROLL_THRESH

            #camera u / d
            if self.rect.bottom > (Constants.SCREEN_HEIGHT - Constants.SCROLL_THRESH):
                screen_scroll[1] = (Constants.SCREEN_HEIGHT - Constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = Constants.SCREEN_HEIGHT - Constants.SCROLL_THRESH
            if self.rect.top < Constants.SCROLL_THRESH:
                screen_scroll[1] = Constants.SCROLL_THRESH - self.rect.top
                self.rect.top = Constants.SCROLL_THRESH

        return screen_scroll

    def ai(self, player, obstacle_tiles, screen_scroll):
        stun_lock = 100
        clipped_line = ()
        ai_dx = 0
        ai_dy = 0

        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #line of sight
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))

        #see if something is in the way
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        #check distance from player
        dist = math.sqrt(((self.rect.centerx - player.rect.centerx) **2)  +  ((self.rect.centery - player . rect.centery)**2))
        if not clipped_line and dist > Constants.RANGE:
            if self.rect.centerx  > player.rect.centerx:
                ai_dx = -Constants.ENEMY_SPEED
            if self.rect.centerx  < player.rect.centerx:
                ai_dx = Constants.ENEMY_SPEED
            if self.rect.centery  > player.rect.centery:
                ai_dy = -Constants.ENEMY_SPEED
            if self.rect.centery  < player.rect.centery:
                ai_dy = Constants.ENEMY_SPEED

        if self.alive:
            if not self.stunlock:
                self.move(ai_dx, ai_dy, obstacle_tiles)
                #ouchie
                if dist < Constants.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()


            #hit?
            if self.hit == True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunlock = True
                self.running = False
                self.update_action(0)
            
            if (pygame.time.get_ticks() - self.last_hit > stun_lock):
                self.stunlock = False



    def update(self):
        #is bro alive
        if self.health <= 0:
            self.health = 0
            self.alive = False 

        #HIT COOLDOWN
        hit_cooldown = 500
        if self.char_type == 0:
            if self.hit == True and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False



        #check what action the player is doing
        if self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)


        animation_cooldown = 70
        #handle animatio
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last image
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if animation is done
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
    def update_action(self, new_action):
        #check if new action is diferent than last one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x - 40 , self.rect.y - Constants.SCALE * Constants.OFFSET))
        else: 
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, Constants.red, self.rect, 1) 
        