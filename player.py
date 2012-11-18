
import pygame, os
from pygame.locals import *
import copy

class Player(pygame.sprite.Sprite):

	speed = 15
	jumpSpeed = 20

	def __init__(self, pos, world):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/player.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.direction = [0,0]
		self.jumpVelocity = 0
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
			self.jumpVelocity = self.jumpSpeed
			self.state = self.enumState.JUMP
		elif keys[pygame.K_s]:
			pass
			#newDir[1] = 1
			#self.state = self.enumState.RUNLEFT
		if keys[pygame.K_a]:
			newDir[0] = -1
			self.state = self.enumState.RUNLEFT
		elif keys[pygame.K_d]:
			newDir[0] = 1
			self.state = self.enumState.RUNRIGHT		

		self.direction = copy.deepcopy(newDir)

	def updatePos(self):
		diagSpecial = 1
		if self.direction[0] != 0 and self.direction[1] != 0:
			diagSpecial = .707

		newPos = [self.rect.center[0] + self.direction[0] * self.speed * diagSpecial, self.rect.center[1] + self.direction[1] * self.speed * diagSpecial]
		self.jumpVelocity -= self.world.gravity
		newPos = [newPos[0], (int)(newPos[1] - self.jumpVelocity)]
		print self.jumpVelocity - self.world.gravity

		self.rect.center = newPos
		

	def enum(*sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		reverse = dict((value, key) for key, value in enums.iteritems())
		enums['reverse_mapping'] = reverse
		return type('Enum', (), enums)