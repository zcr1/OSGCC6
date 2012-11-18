#OSGCC 6 a

import pygame, sys
from player import *
from world import *
from level import *

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

if __name__ == '__main__':
	main()