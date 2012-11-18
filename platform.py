
import pygame, os
from pygame.locals import *
import copy
import math

class Platform(pygame.sprite.Sprite):


	maxDisplacement = 800
	moveInc = 3

	def __init__(self, pos, death, number, move):
		pygame.sprite.Sprite.__init__(self)
		filepath = "/osgcc/images/newplatform" + number + ".png"
		#print filepath
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + filepath

		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.worldPos = pos
		self.death = (int)(death)
		self.currDisplacement = 0
		self.moveX = False
		self.moveY = False
		self.direction = [0,0]
		self.active = False
		self.acceleration = 1
		self.type = move
		self.gravyVent = False
		if move == 1:
			self.moveX = True
			self.direction = [1,0]
		elif move == 2:
			self.moveY = True
			self.direction = [0,1]
		elif move == 3:
			self.moveX = True
			self.moveY = True
			self.direction = [1,1]
		elif move == 4: #vent of gravy
			self.gravyVent = True

	def Update(self):
		pass

	def isFall(self):
		if self.type == 4:
			return True

	def Active(self):
		self.direction = [0,1]
		self.acceleration = 1

	def updatePos(self):
		delta = self.moveInc
		if self.currDisplacement < self.maxDisplacement:
			self.currDisplacement += delta
			if self.currDisplacement > self.maxDisplacement:
				self.currDisplacement = self.maxDisplacement
				delta = self.currDisplacement - self.maxDisplacement
			self.worldPos[1] += delta * self.direction[1] * self.acceleration
			self.worldPos[0] += delta * self.direction[0]
		elif self.currDisplacement == self.maxDisplacement:
			self.direction[1] = - self.direction[1] * self.acceleration
			self.direction[0] = - self.direction[0]
			self.currDisplacement = 0
			
			


