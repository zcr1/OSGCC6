
import pygame, os
from pygame.locals import *
from bean import *
import copy
import math
import spritesheet
from sprite_strip_anim import SpriteStripAnim

class Player(pygame.sprite.Sprite):

	speedMax = 20
	speedInc = 4
	jumpSpeed = 20
	friction = .9
	shotDelay = .1

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
		self.strips = [SpriteStripAnim('images/chickenrun.png', (0,0,100,100), 6, 0, True, 5),
			SpriteStripAnim('images/chickenrun.png', (0,0,100,100), 6, 0, True, 5),
 			SpriteStripAnim('images/chickenrun.png', (0,0,100,100), 6, 0, True, 5),
 			SpriteStripAnim('images/chickenrun.png', (0,0,100,100), 6, 0, True, 5)
		]
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
		self.enumState = self.enum(STAND=0, RUNLEFT=1, RUNRIGHT=2, JUMP=3)
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
			newDir[1] = -1
			self.jumpVel = self.jumpSpeed
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
		if self.direction[0] != 0 and self.direction[1] != 0:
			diagSpecial = .707
		deltaHoriz = self.horizVel * diagSpecial  * self.friction
		if self.horizVel < 0:
			self.horizVel =  math.ceil(self.horizVel * self.friction)
		else:
			self.horizVel = self.horizVel * self.friction	
		newPos = [self.rect.center[0] + deltaHoriz, self.rect.center[1] + self.direction[1] * diagSpecial]

		self.jumpVel -= self.world.gravity
		newPos = [newPos[0], (int)(newPos[1] - self.jumpVel)]

		self.rect.center = newPos
		self.worldPos = newPos
		self.updateSpriteSheet()
		
	def Fire(self):
		secs = self.world.clock.tick() / 1000.0
		if (secs + self.lastShot) > self.shotDelay:
			self.lastShot = 0
			return Bean(self.rect.center, self.worldPos, self.direction)
		else:
			self.lastShot += secs
			return None

	def updateState(self, state):
		self.enumsSate = state
		if(self.state != state):
			self.stateChanged = 1


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