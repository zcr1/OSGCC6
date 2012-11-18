#OSGCC 6 

import pygame, sys
from player import *
from enemy import *
from world import *
from level import *
import random

def main():
	
	clock = pygame.time.Clock()
	FPS = 30
	world = World()
	player = Player([400,400], world)
##	enemy = Enemy([810 ,int(round(random.random() * 1000))], world)
	enemy = Enemy([810, 400], world)
	level = Level(world)
	world.addPlayer(player)
	world.addEnemy(enemy)
	world.setLevel(level)

	while True:
		world.Update()
		pygame.display.update()
		clock.tick(FPS)

if __name__ == '__main__':
	main()
