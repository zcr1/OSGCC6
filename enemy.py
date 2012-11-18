import pygame, os
from pygame.locals import *
import copy
import math

class Enemy(pygame.sprite.Sprite):

	speedMax = 20
	speedInc = 4
	jumpSpeed = 20
	friction = .9
	
	def __init__(self, pos, world):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/enemy.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.worldPos = pos
		self.direction = [0,0]
		self.jumpVel = 0
		self.horizVel = 0
		self.stateChange = 0

		self.world = world
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
		self.enumState = self.enum(STAND=0, RUNLEFT=1, RUNRIGHT=2, JUMP=3)
		self.state = self.enumState.STAND

	#do updates
	def Update(self, keys):
		self.parseKeys(keys)
		self.updatePos()

	def parseKeys(self, keys):
		newDir = [0,0]

		if keys[pygame.K_w]:
			newDir[1] = -1
			self.jumpVel = self.jumpSpeed
			self.state = self.enumState.JUMP
		elif keys[pygame.K_s]:
			pass
			#newDir[1] = 1
			#self.state = self.enumState.RUNLEFT
		if keys[pygame.K_a]:
			newDir[0] = -1
			self.state = self.enumState.RUNLEFT
			self.horizVel -= self.speedInc
			if self.horizVel < -self.speedMax:
				self.horizVel = -self.speedMax
			

		elif keys[pygame.K_d]:
                        

                        
			newDir[0] = 1
			self.state = self.enumState.RUNRIGHT	
			self.horizVel += self.speedInc
			if self.horizVel > self.speedMax:
				self.horizVel = self.speedMax	

		self.direction = copy.deepcopy(newDir)
		
		self.direction = [1,0]
		self.state = self.enumState.RUNLEFT
		self.horizVel -= self.speedInc
		self.horizVel = -self.speedMax
		
##		if keys[pygame.K_a]:
##			newDir[0] = -1
##			self.state = self.enumState.RUNLEFT
##			self.horizVel -= self.speedInc
##			if self.horizVel < -self.speedMax:
##				self.horizVel = -self.speedMax

	def updatePos(self):
               	diagSpecial = 1
		if self.direction[0] != 0 and self.direction[1] != 0:
			diagSpecial = .707
		deltaHoriz = self.horizVel * diagSpecial  * self.friction
		if self.horizVel < 0:
			self.horizVel =  math.ceil(self.horizVel * self.friction)
		else:
			self.horizVel = self.horizVel * self.friction	
		newPos = [self.rect.center[0] + deltaHoriz, self.rect.center[1] + self.direction[1] * diagSpecial]

		#self.jumpVel -= self.world.gravity
		#newPos = [newPos[0], (int)(newPos[1] - self.jumpVel)]

		self.rect.center = newPos
		self.worldPos = newPos
		

	def enum(*sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		reverse = dict((value, key) for key, value in enums.iteritems())
		enums['reverse_mapping'] = reverse
		return type('Enum', (), enums)

	    
