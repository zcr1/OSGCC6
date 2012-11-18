
import pygame, os
from pygame.locals import *
import copy
import math

class Platform(pygame.sprite.Sprite):


	def __init__(self, pos , height, width, death, number):
		pygame.sprite.Sprite.__init__(self)
		filepath = "/osgcc/images/newplatform" + number + ".png"
		print filepath
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + filepath
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.worldPos = pos
		self.height = height;
		self.width = width;

		self.death = death


	def Update(self):
		pass
