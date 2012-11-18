
import pygame, os
from pygame.locals import *
import copy

class Player(pygame.sprite.Sprite):

	speed = 15
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/player.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.direction = [0,0]

	#do updates
	def Update(self, keys):
		self.parseKeys(keys)
		self.updatePos()

	def parseKeys(self, keys):
		newDir = [0,0]

		if keys[pygame.K_w]:
			newDir[1] = -1
		elif keys[pygame.K_s]:
			newDir[1] = 1
		if keys[pygame.K_a]:
			newDir[0] = -1
		elif keys[pygame.K_d]:
			newDir[0] = 1
		self.direction = copy.deepcopy(newDir)

	def updatePos(self):
		diagSpecial = 1
		if self.direction[0] != 0 and self.direction[1] != 0:
			diagSpecial = .707

		self.rect = self.rect.move(self.direction[0] * self.speed * diagSpecial, self.direction[1] * self.speed * diagSpecial)