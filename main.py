#OSGCC 6 

import pygame, sys
from player import *
from world import *

def main():
	
	clock = pygame.time.Clock()
	FPS = 30
	world = World()
	player = Player([100,100], world)
	world.addPlayer(player)
	while True:
		world.Update()
		pygame.display.update()
		clock.tick(FPS)

if __name__ == '__main__':
	main()
