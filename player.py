
import pygame, os
from pygame.locals import *
from bean import *
import copy
import math
import spritesheet
from sprite_strip_anim import SpriteStripAnim

class Player(pygame.sprite.Sprite):

	speedMax = 10
	speedInc = 2
	jumpSpeed = 10
	friction = .9
	shotDelay = .1
	maxFall = 30

	def __init__(self, pos, world):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/chicken.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.worldPos = pos
		self.direction = [0,0]
		self.jumpVel = 0
		self.horizVel = 0
		self.lastShot = 0
		self.statechanged = 0
		self.world = world
		self.dead = False
		self.grounded = False
		self.jump = False
		self.strips = [SpriteStripAnim('images/chickenidle.png', (0,0,100,100), 4, (16, 16, 16), True, 5),
			SpriteStripAnim('images/chickenrunL.png', (0,0,100,100), 6, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenrun2.png', (0,0,100,100), 6, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenjump.png', (0,0,100,100), 2, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenjumpR.png', (0,0,100,100), 2, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenspit.png', (0,0,100,100), 1, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenspit.png', (100,0,100,100), 1, (16, 16, 16), True, 5)
		]
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
		self.enumState = self.enum(STAND=0, RUNLEFT=1, RUNRIGHT=2, JUMPLEFT=3, JUMPRIGHT=4, SHOOTL=5, SHOOTR=6)
		self.state = -1
		self.updateState(self.enumState.STAND)
		self.HP = 10

	#do updates
	def Update(self, keys):
		self.parseKeys(keys)
		self.updatePos()

	def parseKeys(self, keys):
		newDir = [0,0]

		if keys[pygame.K_w]:
			#if not self.jump:
			self.jump = True
			self.jumpVel = self.jumpSpeed
			self.state = self.enumState.JUMP
			newDir[1] = -1
			self.updateState(self.enumState.JUMP)

		elif keys[pygame.K_s]:
			pass
			#newDir[1] = 1
			#self.updateState(self.enumState.RUNLEFT)
		if keys[pygame.K_a]:
			newDir[0] = -1
			self.updateState(self.enumState.RUNLEFT)
			self.horizVel -= self.speedInc
			if self.horizVel < -self.speedMax:
				self.horizVel = -self.speedMax
		elif keys[pygame.K_d]:
			newDir[0] = 1
			self.updateState(self.enumState.RUNRIGHT)	
			self.horizVel += self.speedInc
			if self.horizVel > self.speedMax:
				self.horizVel = self.speedMax
		if keys[pygame.K_SPACE]:
			bean = self.Fire()
			if bean:
				self.world.objects.add(bean)	

		self.direction = copy.deepcopy(newDir)

	def updatePos(self):
		diagSpecial = 1

		#if self.direction[0] != 0 and self.direction[1] != 0:
		#	diagSpecial = .707
		
		deltaHoriz = self.horizVel * diagSpecial  * self.friction

		if self.horizVel < 0:
			self.horizVel =  math.ceil(self.horizVel * self.friction)
		else:
			self.horizVel = self.horizVel * self.friction	

		newPos = [self.worldPos[0] + deltaHoriz, self.worldPos[1]]

		if not self.grounded:
			self.jumpVel -= self.world.gravity
			if self.jumpVel < -self.maxFall:
				self.jumpVel = -self.maxFall

		newPos = [newPos[0], (int)(newPos[1] - (self.jumpVel * diagSpecial))]

		collisionObj = self.world.checkCollision(self, newPos)
		if collisionObj:
			if collisionObj.death == 1:
				self.dead = True
			elif newPos[1] > self.worldPos[1]:
				self.jump = False
				self.jumpVel = 0
				self.grounded = True
				#newPos[1] = copy.deepcopy(collisionObj.rect.top)
		else: 
			self.grounded = False

		self.worldPos = newPos
		self.updateSpriteSheet()
		
	def Fire(self):
		secs = self.world.clock.tick() / 1000.0
		if (secs + self.lastShot) > self.shotDelay:
			self.lastShot = 0
			return Bean(self.rect.center, self.worldPos, self.direction, self.world)
		else:
			self.lastShot += secs
			return None

	def updateState(self, state):
		if(self.state != state):
			self.stateChanged = 1
		self.state = state

	def updateSpriteSheet(self):
		n = (int)(self.state)
		if (self.stateChanged==1):
			self.strips[n].iter()
			self.image = self.strips[n].next()
			self.stateChanged = 0
		else:
			self.image = self.strips[(int)(self.state)].next()

	def enum(*sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		reverse = dict((value, key) for key, value in enums.iteritems())
		enums['reverse_mapping'] = reverse
		return type('Enum', (), enums)