
import pygame
import os
import copy
from math import sin, cos, atan, hypot

class Bean(pygame.sprite.Sprite):
	pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
	robotdie = pygame.mixer.Sound("sounds/robot-die.wav")
	speed = 30
	durationMax = 1

	def __init__(self, localPos, worldPos, direction, world, enemy):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/OSGCC6/images/bean.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = copy.deepcopy(localPos)
		self.worldPos = copy.deepcopy(worldPos)
		self.direction = copy.deepcopy(direction)
		self.duration = 0
		self.clock = pygame.time.Clock()
		self.world = world
		if self.direction[0] == 0:
			self.direction[0] = 1;
		self.direction[1] = 0

		self.enemy = enemy

		#self.Rotate()


	def Update(self):
		self.duration += self.clock.tick() / 1000.0
		if self.duration > self.durationMax:
			return False
		self.updatePos()
		if self.enemy: #shot from enemy not player
			return True
		else:
			if self.world.level.checkCollisionEnemy(self):
				self.robotdie.play()
				self.kill()

		return True
	def updatePos(self):
		deltaX = deltaY = 0
		deltaX = self.direction[0] * self.speed
		deltaY = self.direction[1] * self.speed
		self.worldPos = [self.worldPos[0] + deltaX, self.worldPos[1] + deltaY]

	#def Rotate(self):
	#	self.image = pygame.transform.rotate(self.image, 57 * self.Direction(self.direction[0], -self.direction[1]))

	'''def Direction(self,x,y):
		PI = 3.141592653589793238462643383
		TwoPI = PI * 2.0
		HalfPI = PI * 0.5
		OneAndHalfPI = PI * 1.5
		if x > 0:
			if y >= 0:
				return atan(y / x)
			else:
				return atan(y / x) + TwoPI
		elif x == 0:
			if y > 0:
				return HalfPI
			elif y == 0:
				return 0
			else:
				return OneAndHalfPI
		else:
			return atan(y / x) + PI		
'''
