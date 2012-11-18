
import pygame, os
from pygame.locals import *
import copy
import math

class Background():
	def __init__(self, img1, img2):
		filepath1 = "/osgcc/images/" + img1
		filepath2 = "/osgcc/images/" + img2
		#print filepath
		imgPath1 = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + filepath1
		imgPath2 = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + filepath2

		self.image1 = pygame.image.load(imgPath1).convert()
		self.image2 = pygame.image.load(imgPath2).convert()

		self.x1 = 0
		self.y = -300

		self.x2 = 1600

	def Update(self):
		pass

	def Draw(self, screen):
		screen.blit(self.image1,(self.x1,self.y))
		screen.blit(self.image2,(self.x2,self.y))

	def updatePos(self, x, y, fraction):
		self.x1 = self.x1 - x * fraction
		if(self.x1 + 1600 < 0):
			self.x1 += 3200
		elif(self.x1 > 1600):
			self.x1 -= 3200

		self.x2 = self.x2 - x * fraction
		if(self.x2 + 1600 < 0):
			self.x2 += 3200
		elif(self.x2 > 1600):
			self.x2 -= 3200

		#rint self.y
		self.y = self.y - y * fraction
		if(self.y > 0):
			self.y = 0
		elif(self.y < -300):
			self.y = -300
