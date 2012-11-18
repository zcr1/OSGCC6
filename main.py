#OSGCC 6 a

import pygame, sys
from player import *
from world import *
from level import *
from menu import *

background = pygame.image.load("images/titlescreen.png")
backgroundRect = background.get_rect()

def main():
	
	clock = pygame.time.Clock()
	FPS = 60
	world = World()
	player = Player([800,450], world)
	level = Level(world)
	world.addPlayer(player)
	world.setLevel(level)
	 

	pygame.mixer.music.load("sounds/game_01.ogg")
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(.3)
	while True:
		if world.Update() == -1:
			world = World()
			player = Player([800,450], world)
			level = Level(world)
			world.addPlayer(player)
			world.setLevel(level)	

		pygame.display.update()
		clock.tick(FPS)


def menuScreen():
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load("sounds/menu_02.ogg")
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(.4)
	surface = pygame.display.set_mode((1600,900)) #0,6671875 and 0,(6) of HDd resoultiondd
	surface.blit(background, backgroundRect)
	f = pygame.font.Font(None, 128)
	surf = f.render("SUPER ROTISSERIE DX.", 1, (255,255,255), (0,0,255))
	surface.blit(surf, backgroundRect)
	menu = Menu()#necessary
	menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
  	menu.set_fontsize(64)#optional
	menu.move_menu(400, 200)#optional
	menu.init(['Start'], surface)#necessary
        #menu.move_menu(0, 0)#optional
 	menu.draw()#necessary
	pygame.key.set_repeat(199,69)#(delay,interval)
	pygame.display.update()
        #surface.blit(background, backgroundRect)

 	while 1:
 		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == pygame.K_RETURN:
					main()                     
				if event.key == pygame.K_ESCAPE:
					pygame.display.quit()
					sys.exit() 
			

if __name__ == '__main__':
	menuScreen()
	#main()
        
