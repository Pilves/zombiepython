from glob import glob
from random import randint
import pygame  
import math

pygame.init()

screen = pygame.display.set_mode((1280,720))
zombieimg = pygame.image.load('zombie1.png').convert_alpha()
a=0
b=0
#ma teen siia ühe muutuse
#birgitti on ilus
class Player():
    def __init__(self):
        self.x = 640
        self.y = 360
        self.width = 40
        self.height = 80
        self.vel = 2
        self.playerimg = pygame.image.load('tank.png').convert_alpha()
        self.playerimg = pygame.transform.scale(self.playerimg, (self.width,self.height))


    
    def playerdraw(self):
        global screen
        screen.blit(self.playerimg, (self.x,self.y,self.width,self.height))
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x <  1280 - self.width:
            self.x += self.vel
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < 720 - self.height:
            self.y += self.vel 


    def collision(self, otherrect):
        
        myrect = self.playerimg.get_rect().move(self.x,self.y)
        return myrect.colliderect(otherrect)

class Zombie():
    def __init__(self):
        self.x = randint(0,1280)
        self.y = randint(0,720)
        self.width = 30
        self.height = 30
        self.vel = 1
        self.img = pygame.transform.scale(zombieimg, (self.width,self.height))
        self.rect = self.img.get_rect()
    
    def zombcollision(self, otherrect):
        
        myrect = self.rect.move(self.x,self.y)
        return myrect.colliderect(otherrect)


    def zombmove(self, all_zombies):
        global player
        newx=self.x
        newy=self.y
        if player.x + player.width/2 > self.x or randint(0,2) == 0: 
            newx = self.x + self.vel
        if player.x +player.width/2 < self.x or randint(0,2) == 0:
            newx = self.x - self.vel
        if player.y +player.height/2 > self.y or randint(0,2) == 0:
            newy = self.y + self.vel
        if player.y +player.height/2 < self.y or randint(0,2) == 0:
            newy = self.y - self.vel
        # check collisions
        myrect = self.rect.move(newx,newy)
        
        collision = False
        for z in all_zombies:
            if z != self:
                if z.zombcollision(myrect):
                    collision = True
                    break
        collision = collision or player.collision(myrect)
        if not collision:
            self.x = newx
            self.y = newy

    def zombturn(self):
        global rot_image_rect
        
        correction_angle = 90
        drawed = pygame.Rect(self.x,self.y,15,15)
        dx, dy = player.x - self.x, player.y - self.y
        angle = math.degrees(math.atan2(-dy, dx)) - correction_angle
        rot_image = pygame.transform.rotate(self.img, angle)
        rot_image_rect = rot_image.get_rect(center = drawed.center)
        screen.blit(rot_image, rot_image_rect)


run = True
player = Player()
zombes= []
for i in range(5):
    zombes.append(Zombie())

while run:
    screen.fill((255,127,80))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for zombe in zombes:

        zombe.zombmove(zombes)
        zombe.zombturn()

    player.move()
    player.playerdraw()


    
    pygame.display.update()
    pygame.display.flip()
    pygame.time.delay(2)


pygame.quit()
