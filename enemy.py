import pygame, os
from pygame.locals import *
import copy
import math

class Enemy(pygame.sprite.Sprite):

	speedMax = 20
	speedInc = 2
	jumpSpeed = 12
	friction = .9
	jumpDelay = 2
	aggroDistance = 300
	
	def __init__(self, pos, world, clock, type):
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
		self.grounded = False

		self.jumper = True

		self.jump = False
		self.deltaJump = 0
		self.aggro = False

		self.world = world
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
		self.enumState = self.enum(STAND=0, RUNLEFT=1, RUNRIGHT=2, JUMP=3)
		self.state = self.enumState.STAND

	#do updates
	def Update(self):

		if self.world.player.worldPos[0] - self.worldPos[0] < self.aggroDistance:
			self.aggro = True
		if self.aggro:
			self.updatePos()


	def updatePos(self):
		if self.jumper: #jump every x seconds
			self.deltaJump += self.clock.tick() / 1000.0
			if self.deltaJump >= self.jumpDelay:
				self.jumpVel = self.jumpSpeed
				self.deltaJump = 0

		if not self.grounded:
			self.jumpVel -= self.world.gravity
		
		newPos = [self.worldPos[0] + self.speedInc, self.worldPos[1] - self.jumpVel] 

		newPos = self.getCollisions(newPos)
		

		self.worldPos = newPos
		

	def getCollisions(self, newPos):
		collisionObj = self.world.checkCollision(self, [self.worldPos[0],newPos[1]])
		if collisionObj:
			if collisionObj.death == 1:
				self.dead = True
			elif newPos[1] > self.worldPos[1]:
				self.jump = False
				self.jumpVel = 0
				self.grounded = True
				#newPos[1] = copy.deepcopy(collisionObj.rect.top)
			elif newPos[1] < self.worldPos[1] and not self.grounded:
				newPos[1] += 10
				self.jumpVel = -2
		else: 
			self.grounded = False



		return newPos


	def enum(*sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		reverse = dict((value, key) for key, value in enums.iteritems())
		enums['reverse_mapping'] = reverse
		return type('Enum', (), enums)

	    
