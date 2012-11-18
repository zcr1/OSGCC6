import pygame, os
from pygame.locals import *
from bean import *
from sprite_strip_anim import SpriteStripAnim
import copy
import math

class Enemy(pygame.sprite.Sprite):

	speedMax = 20
	speedInc = 5
	jumpSpeed = 12
	friction = .9
	jumpDelay = 1.25
	aggroDistance = 600
	shotDelay = .5
	mouthjump = pygame.mixer.Sound("sounds/mouth-jump.wav")

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
		self.stateChanged = 0
		self.clock = clock
		self.grounded = False
		self.type = type
		self.lastShot = 0
		self.shooter = False

		#0 = rolly gion' left
		#1 = rolly goin' right
		#3 = hoppy-ass dude 
		self.strips = [SpriteStripAnim('images/enemy0.png', (0,0,100,100), 2, (16, 16, 16), True, 15),
			SpriteStripAnim('images/enemy0.png', (0,100,100,100), 2, (16, 16, 16), True, 15),
			SpriteStripAnim('images/enemy1.png', (0,0,100,100), 1, (16, 16, 16), True, 15)
		]
		self.enumState = self.enum(ROLLLEFT=0, ROLLRIGHT=1, JUMPER=2)
		self.state = -1
		if type == 0:
			self.updateState(self.enumState.ROLLLEFT)
			self.shooter = True
		if type == 2:
			self.shooter = False
			self.updateState(self.enumState.JUMPER)
		if type == 1:
			self.jumper = True
			self.updateState(self.enumState.JUMPER)
		else:
			self.jumper = False

		self.updateSpriteSheet()
		self.jump = False
		self.deltaJump = 0
		self.aggro = False

		self.world = world
		#http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python

	#do updates
	def Update(self):
		if self.aggro:
			self.secs = self.world.clock.tick() / 1000.0
			if self.shooter:
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
				self.mouthjump.play()

		if not self.grounded:
			self.jumpVel -= self.world.gravity
		else:
			self.jumpVel = 0
		
		deltaX = self.direction[0] * self.speedInc
		newPos = [self.worldPos[0] + deltaX, self.worldPos[1] - self.jumpVel] 

		flag = False
		newPos = self.getCollisions(newPos, flag)
		
		self.worldPos = newPos

		if not self.jumper and self.grounded:
			self.simulateAhead()

		self.updateSpriteSheet()

	def simulateAhead(self):
		
		deltaX = self.direction[0] * self.speedInc * 5
		newPos = [self.worldPos[0] + deltaX, self.worldPos[1] - self.jumpVel] 
		flag = True
		newPos = self.getCollisions(newPos, flag)
		#if newPos[1] != self.worldPos[1]:
		if not self.grounded:
			self.direction[0] = -self.direction[0]	
			self.updateState(not self.state)

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

	def getCollisions(self, newPos, flag):
		#y
		if flag:
			collisionObj = self.world.checkCollision(self, [newPos[0],newPos[1]])
		else:
			collisionObj = self.world.checkCollision(self, [self.worldPos[0],newPos[1]])
		if collisionObj:
			if collisionObj.death == 1:
				self.dead = True
			elif collisionObj.type == 4:
				self.jumpVel =+ 15
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
				elif collisionObj.type == 4:
					self.jumpVel =+ 15
				elif newPos[0] > self.worldPos[0]:
					newPos[0] -= 10
				elif newPos[0] < self.worldPos[0]:
					newPos[0] += 10

		collisionObj = self.world.level.checkCollisionMoving(self, [self.worldPos[0],newPos[1]])		
		if collisionObj:
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




		#if collides with another enemy reverse direction
		if not flag:
			collisionObj = self.world.level.checkEnemyCollision(self, newPos)
			if collisionObj:
				self.direction[0] = -self.direction[0]

		if newPos[1] > 3000:
			self.kill()
		return newPos


	def enum(*sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		reverse = dict((value, key) for key, value in enums.iteritems())
		enums['reverse_mapping'] = reverse
		return type('Enum', (), enums)

	    
