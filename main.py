import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

# Background dimensions
screen_height = 812
screen_width = 375

#Game Variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

# Load Background and Scrolling Ground
bg_image = pygame.image.load("sprites/background-day.png")
bg_image = pygame.transform.scale(bg_image, (375, 680))
bg_rect = bg_image.get_rect()
ground_image = pygame.image.load("sprites/base.png")
ground_image = pygame.transform.scale(ground_image, (400, 140))
bg_rect = bg_image.get_rect()

# Initiate the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.images.append(pygame.image.load("sprites/redbird-upflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-upflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-upflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-upflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-midflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-midflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-midflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-midflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-midflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.images.append(pygame.image.load("sprites/redbird-downflap.png"))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        global flying
        global game_over

        if not game_over:
            if flying:
                self.vel += .5
                if self.vel > 8:
                    self.vel = 8
            if self.rect.y <= 660:
                self.animate_bird()
                self.rect.y += self.vel
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -80)
                flying = False
                game_over = True

            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.rect.y > 0:
                self.vel = -10
                self.clicked = True
                self.image = pygame.transform.rotate(self.images[self.index], 25)

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

    def animate_bird(self):
        #Animate Wings
        if not game_over:
            self.image = self.images[self.index]
            self.index += 1
            if self.index == len(self.images):
                self.index = 0
            
            #Animate Rotation.
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2.5)


bird_group = pygame.sprite.Group()

flappy = Bird(50, screen_height // 2)
bird_group.add_internal(flappy)


run = True
while run == True:
    #Set the framerate
    clock.tick(60)

    #Draw the background
    screen.blit(bg_image, (0,0), bg_rect)

    bird_group.draw(screen)
    bird_group.update()

    #Draw and scroll the ground
    screen.blit(ground_image, (ground_scroll, 680))
    if not game_over:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 25:
            ground_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    
    pygame.display.update()

# if __file__ == '__main__':
#     flappybird.play()