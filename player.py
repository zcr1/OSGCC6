
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
	maxJumps = 2
	#maxJumps = 20
	#speedMax = 20
	#speedInc = 5
	jumpSpeed = 12
	friction = .9
	shotDelay = .4
	maxFall = 30
	shotDisplayDelay = .5
	invulnEnemyDuration = 1.0
	jumpGap = .25
	gravyVent = 20
	damage = pygame.mixer.Sound("sounds/damage_01.wav")
	littleparp = pygame.mixer.Sound("sounds/little-parp.wav")



	def __init__(self, pos, world):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/chicken.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.worldPos = pos
		self.direction = [0,0]
		self.faceDir = [0,0]
		self.jumpVel = 0
		self.horizVel = 0
		self.lastShot = 0
		self.statechanged = 0
		self.shootstatetimer = 0
		self.world = world
		self.dead = False
		self.grounded = False
		self.jump = False
		self.invulnDuration = 0
		self.jumpCount = 0
		self.jumpDuration = 10
		self.onPlatform = False
		self.delayFall = 0

		self.clock = pygame.time.Clock()
		self.strips = [SpriteStripAnim('images/chickenidle.png', (0,0,100,100), 4, (16, 16, 16), True, 5),
			SpriteStripAnim('images/chickenrunL.png', (0,0,100,100), 6, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenrun2.png', (0,0,100,100), 6, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenjump.png', (0,0,100,100), 2, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenjumpR.png', (0,0,100,100), 2, (16, 16, 16), True, 5),
 			SpriteStripAnim('images/chickenspit.png', (100,0,100,100), 1, (16, 16, 16), True, 50),
 			SpriteStripAnim('images/chickenspit.png', (0,0,100,100), 1, (16, 16, 16), True, 50)
		]
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
		self.enumState = self.enum(STAND=0, RUNLEFT=1, RUNRIGHT=2, JUMPLEFT=3, JUMPRIGHT=4, SHOOTL=5, SHOOTR=6)
		self.state = -1
		self.updateState(self.enumState.STAND)
		self.hp = 5




	#do updates
	def Update(self, keys):
		secs = self.clock.tick()/1000.0
		if self.grounded == False:
			self.updateState(self.enumState.JUMPRIGHT)
		self.jumpDuration += secs
		self.shootstatetimer  -= secs
		self.invulnDuration -= secs
		if self.invulnDuration < 0:
			self.invulnDuration = 0
		self.parseKeys(keys)
		self.updatePos()
		if self.world.level.reieveCheckCollisionEnemy(self):
			if not self.invulnDuration > 0:
				self.hp -= 1
				if self.hp == 0:
					self.dead = True
				self.invulnDuration = self.invulnEnemyDuration




	def parseKeys(self, keys):
		newDir = [0,0]

		if keys[pygame.K_w]:
			if self.jumpDuration > self.jumpGap:
				self.jumpDuration = 0
				self.jumpCount += 1
				if self.jumpCount <= self.maxJumps:
					self.jump = True
					self.jumpVel = self.jumpSpeed
					newDir[1] = -1
					self.updateState(self.enumState.JUMPLEFT)

		elif keys[pygame.K_s]:
			pass
			#newDir[1] = 1
			#self.updateState(self.enumState.RUNLEFT)
		if keys[pygame.K_a]:
			newDir[0] = -1
			self.faceDir[0] = -1
			self.updateState(self.enumState.RUNLEFT)
			self.horizVel -= self.speedInc
			if self.horizVel < -self.speedMax:
				self.horizVel = -self.speedMax
		elif keys[pygame.K_d]:
			newDir[0] = 1
			self.faceDir[0] = 1
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
		deltaHoriz = self.horizVel * diagSpecial  * self.friction

		if self.horizVel < 0:
			self.horizVel =  math.ceil(self.horizVel * self.friction)
		else:
			self.horizVel = self.horizVel * self.friction	

		if(abs(self.horizVel) < 1):
			self.horizVel = 0

		newPos = [self.worldPos[0] + deltaHoriz, self.worldPos[1]]

		if not self.grounded:
			self.jumpVel -= self.world.gravity
			if self.jumpVel < -self.maxFall:
				self.jumpVel = -self.maxFall

		newPos = [newPos[0], (int)(newPos[1] - (self.jumpVel * diagSpecial))]

		newPos = self.getCollisions(newPos)
		self.world.level.bg1.updatePos(newPos[0]-self.worldPos[0], newPos[1]-self.worldPos[1], .1)
		self.worldPos = newPos
		self.updateSpriteSheet()




	def getCollisions(self, newPos):
		#y direction
		collisionObj = self.world.checkCollision(self, [self.worldPos[0],newPos[1]])
		if collisionObj:
			if collisionObj.death == 1:
				self.dead = True
			elif collisionObj.type == 4:
				self.jumpVel =+ self.gravyVent
				collisionObj.switchImage("11")
				self.jumpCount = 0
			elif newPos[1] > self.worldPos[1]:
				self.jump = False
				self.jumpVel = 0
				self.grounded = True
				self.jumpCount = 0
				#newPos[1] = copy.deepcopy(collisionObj.rect.top)
			elif newPos[1] < self.worldPos[1] and not self.grounded:
				newPos[1] += 10
				self.jumpVel = -2
		else: 
			self.grounded = False
		#x  direction
		collisionObj = self.world.checkCollision(self, [newPos[0], self.worldPos[1]])
		if collisionObj and not self.grounded:
			if collisionObj.death == 1:
				self.dead = True
			elif collisionObj.type == 4:
				self.jumpVel =+ 15
				self.jumpCount = 0
			elif newPos[0] > self.worldPos[0]:
				newPos[0] -= 10
			elif newPos[0] < self.worldPos[0]:
				newPos[0] += 10

		collisionObj = self.world.level.checkEnemyCollision(self, newPos)
		if collisionObj:
			if newPos[1] < collisionObj.worldPos[1] and not self.grounded:
				self.damage.play()
				collisionObj.kill()
				self.jump = True
				self.jumpVel = self.jumpSpeed
			else:
				if not self.invulnDuration > 0:
					self.damage.play()
					self.hp -= 1
					if self.hp == 0:
						self.dead = True
					self.invulnDuration = self.invulnEnemyDuration

		

		collisionObj = self.world.level.checkItemCollision(self, newPos)
		if collisionObj:
			if collisionObj.type == 0: #+ hp
				self.hp += 1
				if self.hp == 0:
					self.dead = True
			collisionObj.kill()
			self.littleparp.play()



		collisionObj = self.world.level.checkCollisionMoving(self, [self.worldPos[0],newPos[1]])		
		if collisionObj:
			if collisionObj.death == 1:
				self.dead = True
			#if collisionObj.isFall():
			#	collisionObj.Active()
			if newPos[1] > self.worldPos[1] and collisionObj.moveY:
				self.jump = False
				if collisionObj.direction[1] == 1:
					self.jumpVel = -3 * collisionObj.acceleration
				else:
					self.jumpVel = 3
				self.grounded = True
				self.jumpCount = 0
			elif newPos[1] > self.worldPos[1]: #platform moving left-right
				if collisionObj.death == 1:
					self.dead = True
				elif newPos[1] > self.worldPos[1]:
					self.jump = False
					self.jumpVel = 0
					self.grounded = True
					self.jumpCount = 0
					newPos[1] -= 1
					#newPos[1] = copy.deepcopy(collisionObj.rect.top)
				elif newPos[1] < self.worldPos[1] and not self.grounded:
					newPos[1] += 10
					self.jumpVel = 0			
			elif newPos[1] < self.worldPos[1] and collisionObj.moveY:
				self.jump = False
				#self.jumpVel = 0
				self.grounded = True
				self.jumpCount = 0
			elif newPos[1] < self.worldPos[1]: #platform moving left-right
				newPos[1] += 10
				self.jumpVel = 0			
		else:
			self.onPlatform = False

		return newPos

		
	def Fire(self):
		secs = self.world.clock.tick() / 1000.0
		if (secs + self.lastShot) > self.shotDelay:
			self.littleparp.play()
			self.lastShot = 0
			if(self.faceDir[0] < 0):
				self.updateState(self.enumState.SHOOTL)
			else:
				self.updateState(self.enumState.SHOOTR)
			self.shootstatetimer = self.shotDisplayDelay
			return Bean([self.rect.center[0], self.rect.center[1]-25], [self.worldPos[0], self.worldPos[1]-25], self.faceDir, self.world, False)

		else:
			self.lastShot += secs
			return None




	def updateState(self, state):
		if(self.shootstatetimer > 0):
			return None;
		if(self.state != state):
			self.stateChanged = 1
		self.state = state




	def updateSpriteSheet(self):
		n = (int)(self.state)

		if(self.shootstatetimer > 0):
			self.image = self.strips[n].next()
			return None;
		if((self.grounded == True and self.horizVel == 0) or (self.horizVel == 0 and self.jumpVel == 0)):
				self.state = self.enumState.STAND
 		if (self.stateChanged==1):
			#if(self.grounded == False and (self.state == self.enumState.RUNLEFT or self.state == self.enumState.RUNRIGHT)):
			if(self.grounded == False and self.faceDir[0] < 0):
				self.state = self.enumState.JUMPLEFT
			elif(self.faceDir[0] > 0 and self.state == self.enumState.JUMPLEFT):
				self.state = self.enumState.JUMPRIGHT
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