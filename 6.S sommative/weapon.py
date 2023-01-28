import pygame, math, Constants, random

class Weapon():
    def __init__(self, image, bullet_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.bullet_image = bullet_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = 300
        bullet = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centerx)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        #get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot):
            bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        #reset mouse click
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

        return bullet
    
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #calculate bullet properties
        self.dx = math.cos(math.radians(self.angle)) * Constants.BULLET_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * Constants.BULLET_SPEED) 

    def update(self, screen_scroll, obstacle_tiles, enemy_list):
        damage = 0
        damage_pos = None

        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.x += self.dx
        self.rect.y += self.dy

        #check if bullet if off screen


        #hit wal?
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()


        #see if bullet hit robo
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break
        
        return damage, damage_pos 

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))


 

