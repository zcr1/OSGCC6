#OSGCC 6 

import pygame, sys
from player import *
from world import *
from level import *

def main():
	
	clock = pygame.time.Clock()
	FPS = 30
	world = World()
	player = Player([400,400], world)
	level = Level()
	world.addPlayer(player)
	world.setLevel(level)

	while True:
		world.Update()
		pygame.display.update()
		clock.tick(FPS)

if __name__ == '__main__':
	main()