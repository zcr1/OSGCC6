import pygame, os
from pygame.locals import *
import copy
import math

class Enemy(pygame.sprite.Sprite):

	speedMax = 20
	speedInc = 4
	jumpSpeed = 20
	friction = .9
	
	def __init__(self, pos, world, clock):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/enemy.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = copy.deepcopy(pos)
		self.worldPos = copy.deepcopy(pos)
		self.direction = [1,0]
		self.jumpVel = 0
		self.horizVel = 0
		self.stateChange = 0
		self.clock = clock

		self.world = world
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
		self.enumState = self.enum(STAND=0, RUNLEFT=1, RUNRIGHT=2, JUMP=3)
		self.state = self.enumState.STAND

	#do updates
	def Update(self):
		self.updatePos()


	def updatePos(self):
		newPos = [self.worldPos[0] + 5, self.worldPos[1]]
		self.worldPos = newPos
		

	def enum(*sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		reverse = dict((value, key) for key, value in enums.iteritems())
		enums['reverse_mapping'] = reverse
		return type('Enum', (), enums)

	    
