import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()

# Background dimensions
screen_height = 812
screen_width = 375

#Define font
font = pygame.font.SysFont("Bauhaus 93", 60, )
white = (255, 255, 255)

#Game Variables
ground_scroll = 0
scroll_speed = 4
pipe_gap = 150
pipe_refresh = 1000 #miliseconds
last_pipe = pygame.time.get_ticks()
flying = False
game_over = False
score = 0
pass_pipe = False
bird_color = "yellow"

# Load Background and Scrolling Ground
bg_image = pygame.image.load("sprites/background-day.png")
bg_image = pygame.transform.scale(bg_image, (375, 680))
bg_rect = bg_image.get_rect()
ground_image = pygame.image.load("sprites/base.png")
ground_image = pygame.transform.scale(ground_image, (400, 140))
bg_rect = bg_image.get_rect()

game_start_image = pygame.image.load("sprites/message.png")
game_start_rect = game_start_image.get_rect()

game_over_image = pygame.image.load("sprites/gameover.png")
game_over_rect = game_over_image.get_rect()

# Initiate the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

def draw_text(text, font, txt_color, x, y):
    img = font.render(text, True, txt_color)
    screen.blit(img, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-upflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-upflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-upflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-upflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-midflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-midflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-midflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-midflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-midflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
        self.images.append(pygame.image.load(f"sprites/{bird_color}bird-downflap.png"))
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
                pygame.mixer.Sound("audio/wing.wav").play().set_volume(0.1)
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

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position) -> None:
        global pipe_gap
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/pipe-green.png")
        self.rect = self.image.get_rect()
        # Position 1:  Pipe coming from the top
        # Position -1: Pipe coming from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (pipe_gap // 2)]
        if position == -1:
            self.rect.topleft = [x, y + (pipe_gap // 2)]

    def update(self):
        global scroll_speed
        if not game_over:
            self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(50, screen_height // 2)
bird_group.add(flappy)



def reset_game():
    global score
    global pass_pipe
    pipe_group.empty()
    bird_group.empty()
    score = 0
    pass_pipe = False
    flappy = Bird(50, screen_height // 2)
    bird_group.add(flappy)


run = True
while run == True:
    #Set the framerate
    clock.tick(60)

    #Draw the background
    screen.blit(bg_image, (0,0), bg_rect)


    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()


    if not game_over and not flying:
        screen.blit(game_start_image, ((screen_width //2) - (game_start_rect.width // 2), 100 ), game_start_rect)

    if game_over:
        screen.blit(game_over_image, ((screen_width //2) - (game_over_rect.width // 2), 200 ), game_over_rect)
        reset_click = False
        if pygame.mouse.get_pressed()[0] == 1:
            reset_game()
            game_over = False
            flying = True

    #Check the score
    if len(pipe_group) > 0:
        if (bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and
            bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and 
            pass_pipe == False):
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pygame.mixer.Sound("audio/point.wav").play().set_volume(0.2)
                pass_pipe = False
        
    draw_text(str(score), font, white, screen_width // 2, 20)

    #Check for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        if game_over == False:
            pygame.mixer.Sound("audio/hit.wav").play()
        game_over = True

    #Draw and scroll the ground
    screen.blit(ground_image, (ground_scroll, 680))
    if not game_over:
        #Scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 25:
            ground_scroll = 0

        #Scroll the pipes:
        if flying:
            now = pygame.time.get_ticks()
            if now - last_pipe > pipe_refresh:
                pipe_offset = random.randint(-125, 125)
                top_pipe = Pipe(screen_width, (screen_height // 2) + pipe_offset, 1)
                btm_pipe = Pipe(screen_width, (screen_height // 2) + pipe_offset, -1)
                pipe_group.add(top_pipe)
                pipe_group.add(btm_pipe)
                last_pipe = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    
    pygame.display.update()

# if __file__ == '__main__':