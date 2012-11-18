
import pygame, os
from pygame.locals import *
import copy
import math

class Item(pygame.sprite.Sprite):


	def __init__(self, pos , height, width, type):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/canOfBeans.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.worldPos = pos
		self.height = height;
		self.width = width;

		self.type = type
		#0 = +hp
		


	def Update(self):
		pass
