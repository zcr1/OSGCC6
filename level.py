
import pygame, os
from pygame.locals import *
from platform import *
from enemy import *
import copy
import math


class Level():

	def __init__(self, world):
		self.world = world
		platformpath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/datafiles/level1.dat"
		f = open(platformpath)

		allLines = f.readlines()
		self.platforms = pygame.sprite.Group()
		self.drawGroup = pygame.sprite.Group() #which sprties are in view to draw

		for i in range (1, len(allLines)):
			words = allLines[i].split(" ")
			x = (int)(words[0])
			y = (int)(words[1])
			plat = Platform([x, y], words[2], words[3], words[4])
			self.platforms.add(plat)


		# Add enemies to level
		enemy_dat_path = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/datafiles/enemy.dat"
		f = open(enemy_dat_path)

		allLines = f.readlines()
		self.enemies = pygame.sprite.Group()

		for i in range (1, len(allLines)):
			words = allLines[i].split(" ")
			x = (int)(words[0])
			y = (int)(words[1])
			enem = Enemy([x, y], self.world)
			self.enemies.add(enem)	


	def Update(self):
		for sprite in self.enemies:
			sprite.Update(None)
		pass

	#check collisions with objects
	def checkCollision(self, obj, newPos):
		newrect = copy.deepcopy(obj.rect)
		newrect.center = newPos
		for platform in self.platforms:
			newPlat = copy.deepcopy(platform.rect)
			newPlat.center = platform.worldPos
			#print newrect.center
			if newrect.colliderect(newPlat):
				return platform
		return None

	def checkCollisionEnemy(self, obj):
		for enemy in self.enemies:
			#newRec = copy.deepcopy(enemy.rect)
			#newRec.center = enemy.worldPos	
			if enemy.rect.colliderect(obj.rect):
			#if newRec.colliderect(obj.rect):
				enemy.kill()
				return True
		return None

	def Draw(self):
		currentPos = copy.deepcopy(self.world.player.worldPos) #players current worldPos
		self.drawGroup.empty()
		#screen = pygame.Rect((currentPos[0] - 800,currentPos[1] + 450),(800,450))

		for platform in self.platforms:
			#platformWorld = pygame.Rect((platform.rect.center[0] - platform.rect.width/2.0, platform.rect.center[1] + platform.rect.height/2.0),(
				#platform.rect.width,platform.rect.height))
			#if screen.colliderect(platformWorld):
			if (platform.worldPos[0] >= (currentPos[0] - 1600)) and (platform.worldPos[0] <= (currentPos[0] + 1600)):
				platform.rect.center = [800 -  (currentPos[0] - platform.worldPos[0]), 450  - (currentPos[1] - platform.worldPos[1])]
				#print platform.rect.center[1]
				#print platform.rect.center
				self.drawGroup.add(platform)
		for obj in self.world.objects:
			if (obj.worldPos[0] >= (currentPos[0] - 2000)) and (obj.worldPos[0] <= (currentPos[0] + 2000)):
				obj.rect.center = [800 -  (currentPos[0] - obj.worldPos[0]), 450  - (currentPos[1] - obj.worldPos[1])]	
				self.drawGroup.add(obj)		
		for obj in self.enemies:
			if (obj.worldPos[0] >= (currentPos[0] - 2000)) and (obj.worldPos[0] <= (currentPos[0] + 2000)):
				obj.rect.center = [800 -  (currentPos[0] - obj.worldPos[0]), 450  - (currentPos[1] - obj.worldPos[1])]	
				self.drawGroup.add(obj)	
		self.drawGroup.draw(self.world.screen)

	