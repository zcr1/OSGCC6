import sys, pygame, glob
from pygame import *
pygame.init()

background = pygame.image.load("backgrounds/bgemeraldhill01.png")
backgroundRect = background.get_rect()
size = (width, height) = background.get_size()

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

class player:
    def __init__(self):
        self.x = 20
        self.y = 150

##        # stuff for when sonic is standing
##        self.std_speed = 10
##        self.std = glob.glob("C:/Python32/Pygames/sonic/sprites/stand/*.png")
##        self.std.sort()
##        self.stdframe = 0
##        self.std_max = len(self.std) - 1

        # stuff for when sonic is standing
        self.std_speed_init = 20
        self.std_speed = self.std_speed_init
        self.std = glob.glob("C:/Python32/Pygames/sonic/sprites/stand/*.png")
        self.std.sort()
        self.std_pos = 0
        self.std_max = len(self.std) - 1
        self.img_stand = pygame.image.load(self.std[0])
        #self.update(0, "standing")
        

        # stuff for when sonic is running
        self.ani_speed_init = 5
        self.ani_speed = self.ani_speed_init
        self.ani = glob.glob("C:/Python32/Pygames/sonic/sprites/run1/*.png")
        self.ani.sort()
        self.ani_pos = 0
        self.ani_max = len(self.ani) - 1
        self.img = pygame.image.load(self.ani[0])
##        self.update(0, "running")

    def update(self, pos, action):

        # Sonic standing?    
        if action == "standing":
            self.std_speed -= 1
            if self.std_speed == 0:
                self.img_stand = pygame.image.load(self.std[self.std_pos])
                self.std_speed = self.std_speed_init
                if self.std_pos >= self.std_max:
                    self.std_pos = 0
                else:
                    self.std_pos += 1

        
        # Sonic running    
        if pos != 0 and action == "running":
            self.ani_speed -= 1
            self.x += pos
            if self.ani_speed == 0:
                self.img = pygame.image.load(self.ani[self.ani_pos])
                self.ani_speed = self.ani_speed_init
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos += 1
            
        screen.blit(self.img, (self.x, self.y))

player1 = player()
pos = 0

while 1:
    screen.fill((255,255,255))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            pos = 5
            action = "running"
        elif event.type == KEYUP and event.key == K_RIGHT:
            pos = 0
            action = "standing"
        elif event.type == KEYDOWN and event.key == K_LEFT:
            pos = -5
            action = "running"
        elif event.type == KEYUP and event.key == K_LEFT:
            pos = 0
            action = "standing"
        else:
            action = "standing"
            

    screen.blit(background, backgroundRect)        

    player1.update(pos, action)

    pygame.display.update()








    
