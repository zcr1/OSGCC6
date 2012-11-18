"""
Sprite strip animator demo
 
Requires spritesheet.spritesheet and the Explode1.bmp through Explode5.bmp
found in the sprite pack at
http://lostgarden.com/2005/03/download-complete-set-of-sweet-8-bit.html
 
I had to make the following addition to method spritesheet.image_at in
order to provide the means to handle sprite strip cells with borders:
 
            elif type(colorkey) not in (pygame.Color,tuple,list):
                colorkey = image.get_at((colorkey,colorkey))
"""
import sys
import pygame
from pygame.locals import Color, KEYUP, K_ESCAPE, K_RETURN
import spritesheet
from sprite_strip_anim import SpriteStripAnim

background = pygame.image.load("images/backgrounds/bgemeraldhill01.png")
backgroundRect = background.get_rect()
size = (width, height) = background.get_size()
 
surface = pygame.display.set_mode(size)
FPS = 30
frames = FPS / 2
strips = [
    SpriteStripAnim('images/chickenrun.png', (0,0,100,100), 6, 0, True, frames)
]
black = Color('white')
clock = pygame.time.Clock()
n = 0
strips[n].iter()
image = strips[n].next()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == KEYUP:
            if e.key == K_ESCAPE:
                sys.exit()
            elif e.key == K_RETURN:
                n += 1
                if n >= len(strips):
                    n = 0
                strips[n].iter()
    surface.fill(black)
    surface.blit(background, backgroundRect)  
    surface.blit(image, (0,0))
    pygame.display.flip()
    image = strips[n].next()
    clock.tick(FPS)
