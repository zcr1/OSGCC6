
import pygame, os
from pygame.locals import *
from platform import *
import copy
import math


class Level():

	def __init__(self, world):
		self.world = world
		platformpath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/datafiles/level1.dat"
		f = open(platformpath)

		allLines = f.readlines()
		self.platforms = pygame.sprite.Group()

		for i in range (1, len(allLines)):
			words = allLines[i].split(" ")
			x = (int)(words[0])
			y = (int)(words[1])
			plat = Platform([x, y], words[2], words[3])
			self.platforms.add(plat)


	def Update(self):
		pass

	def Draw(self):
		
		self.platforms.draw(self.world.screen)