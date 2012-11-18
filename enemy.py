import pygame, os
from pygame.locals import *
from bean import *
import copy
import math

class Enemy(pygame.sprite.Sprite):

	speedMax = 20
	speedInc = 5
	jumpSpeed = 12
	friction = .9
	jumpDelay = 2
	aggroDistance = 300
	shotDelay = .5
	
	#enemey type, 0=walk, 1=jump, 2=shoot 3= 4=
	def __init__(self, pos, world, clock, type):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/enemy1.png"
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
		self.type = type
		self.lastShot = 0


		if type == 2:
			self.shooter = True
		else:
			self.shooter = False
		if type == 1:
			self.jumper = True
		else:
			self.jumper = False

		self.jump = False
		self.deltaJump = 0
		self.aggro = False

		self.world = world
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
		self.enumState = self.enum(STAND=0, RUNLEFT=1, RUNRIGHT=2, JUMP=3)
		self.state = self.enumState.STAND

	#do updates
	def Update(self):
		if self.aggro:
			self.secs = self.world.clock.tick() / 1000.0
			self.Fire()
			self.updatePos()

		else:
			if math.fabs(self.world.player.worldPos[0] - self.worldPos[0]) < self.aggroDistance:
				self.aggro = True
				if self.world.player.worldPos[0] > self.worldPos[0]:
					self.direction[0] = 1
				else:
					self.direction[0] = -1


	def Fire(self):
		if (self.secs + self.lastShot) > self.shotDelay:
			self.lastShot = 0
			self.world.enemyObjects.add(Bean(self.rect.center, self.worldPos, self.direction, self.world, True))
		else:
			self.lastShot += self.secs
			return None


	def updatePos(self):

		if self.jumper: #jump every x seconds
			self.deltaJump += self.clock.tick() / 1000.0
			if self.deltaJump >= self.jumpDelay:
				self.jumpVel = self.jumpSpeed
				self.deltaJump = 0

		if not self.grounded:
			self.jumpVel -= self.world.gravity
		
		deltaX = self.direction[0] * self.speedInc
		newPos = [self.worldPos[0] + deltaX, self.worldPos[1] - self.jumpVel] 

		flag = False
		newPos = self.getCollisions(newPos, flag)
		
		self.worldPos = newPos

		if not self.jumper and self.grounded:
			self.simulateAhead()


	def simulateAhead(self):
		
		deltaX = self.direction[0] * self.speedInc * 5
		newPos = [self.worldPos[0] + deltaX, self.worldPos[1] - self.jumpVel] 
		flag = True
		newPos = self.getCollisions(newPos, flag)
		#if newPos[1] != self.worldPos[1]:
		if not self.grounded:
			self.direction[0] = -self.direction[0]	

		

	def getCollisions(self, newPos, flag):
		#y
		if flag:
			collisionObj = self.world.checkCollision(self, [newPos[0],newPos[1]])
		else:
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

		#x
		if not flag:
			collisionObj = self.world.checkCollision(self, [newPos[0], self.worldPos[1]])
			if collisionObj and not self.grounded:
				if collisionObj.death == 1:
					self.dead = True
				elif newPos[0] > self.worldPos[0]:
					newPos[0] -= 10
				elif newPos[0] < self.worldPos[0]:
					newPos[0] += 10

		#if collides with another enemy reverse direction
		if not flag:
			collisionObj = self.world.level.checkEnemyCollision(self, newPos)
			if collisionObj:
				self.direction[0] = -self.direction[0]
		return newPos


	def enum(*sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		reverse = dict((value, key) for key, value in enums.iteritems())
		enums['reverse_mapping'] = reverse
		return type('Enum', (), enums)

	    
