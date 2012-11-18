#OSGCC 6 a

import pygame, sys
from player import *
from world import *
from level import *
from menu import *
background = pygame.image.load("images/menu_background.jpg")
backgroundRect = background.get_rect()

def main():
	
	clock = pygame.time.Clock()
	FPS = 60
	world = World()
	player = Player([800,450], world)
	level = Level(world)
	world.addPlayer(player)
	world.setLevel(level)

	while True:
		world.Update()
		pygame.display.update()
		clock.tick(FPS)


def menuScreen():
        surface = pygame.display.set_mode((1600,900)) #0,6671875 and 0,(6) of HD resoultion
        surface.blit(background, backgroundRect)
        f = pygame.font.Font(None, 128)
        surf = f.render("SUPER ROTISSERIE DX.", 1, (255,255,255), (0,0,255))
        surface.blit(surf, backgroundRect)
        menu = Menu()#necessary
        menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
        menu.set_fontsize(64)#optional
        #menu.set_font('data/couree.fon')#optional
        menu.move_menu(400, 200)#optional
        menu.init(['Start','Options','Quit'], surface)#necessary
        #menu.move_menu(0, 0)#optional
        menu.draw()#necessary
    
        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        #surface.blit(background, backgroundRect)
        while 1:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_w:
                            menu.draw(-1) #here is the Menu class function
                        if event.key == K_s:
                            menu.draw(1) #here is the Menu class function
                        if event.key == K_RETURN:
                            if menu.get_position() == 0:#here is the Menu class function
                                main()
                            if menu.get_position() == 2:#here is the Menu class function
                                pygame.display.quit()
                                sys.exit()                        
                        if event.key == K_ESCAPE:
                            pygame.display.quit()
                            sys.exit()
                        pygame.display.update()
                    elif event.type == QUIT:
                        pygame.display.quit()
                        sys.exit()

if __name__ == '__main__':
	#menuScreen()
	main()
        
