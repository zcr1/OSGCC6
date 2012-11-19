import pygame
import os
import random
class World():
	size = width, height = 1600, 900
	gravity = .4
	def __init__(self):
		self.screen = pygame.display.set_mode(self.size)
		self.objects = pygame.sprite.Group() #hold random objects/sprites
		self.enemyObjects = pygame.sprite.Group()
		self.players = pygame.sprite.Group()
		self.player = None
		self.clock = pygame.time.Clock()

		self.playerFlip = True

		self.gameOverFlag = 0
		self.gameOverCount = 0

	#gets called by main game loop to do everything
	def Update(self):
		self.getEvents()
		if self.player.dead:
			self.gameOver()
			return -1
		if self.player.win:
			self.gameWon()
			return -1

		self.Draw()
		self.level.Update()
		for obj in self.objects:
			if not obj.Update():
				obj.kill()
		for obj in self.enemyObjects:
			if not obj.Update():
				obj.kill()



	def gameWon(self):
		count = 0
		while count < 4:
			background = pygame.image.load("images/winscreen1.png")
			backgroundRect = background.get_rect()
			self.screen.blit(background, backgroundRect)
			pygame.display.update()
			pygame.time.delay(300)
			background = pygame.image.load("images/winscreen2.png")
			backgroundRect = background.get_rect()
			self.screen.blit(background, backgroundRect)
			pygame.display.update()
			pygame.time.delay(300)
			background = pygame.image.load("images/winscreen3.png")
			backgroundRect = background.get_rect()
			self.screen.blit(background, backgroundRect)
			pygame.display.update()
			pygame.time.delay(300)
			background = pygame.image.load("images/winscreen4.png")
			backgroundRect = background.get_rect()
			self.screen.blit(background, backgroundRect)
			pygame.display.update()
			pygame.time.delay(300)
			count += 1


	def gameOver(self):
		while self.gameOverCount < 100:
			pygame.font.init()
			fontPos = [random.randint(0,1200), random.randint(0,800)]
			if self.gameOverFlag == 0:
				self.screen.fill(pygame.Color(224,24,13))
				fontobj = pygame.font.Font(None,80)
				msg = fontobj.render("YOU ARE LOSE", 1, (0,0,0))
				self.screen.blit(msg,fontPos, area=None, special_flags=0)
			elif self.gameOverFlag == 1:
				self.screen.fill(pygame.Color(240,38,240))
				fontobj = pygame.font.Font(None,80)
				msg = fontobj.render("YOU ARE LOSE", 1, (224,24,13))
				self.screen.blit(msg,fontPos, area=None, special_flags=0)
			elif self.gameOverFlag == 2:
				self.screen.fill(pygame.Color(40,10,230))
				fontobj = pygame.font.Font(None,80)
				msg = fontobj.render("YOU ARE LOSE", 1, (255,255,255))
				self.screen.blit(msg,fontPos, area=None, special_flags=0)
			self.gameOverFlag += 1
			if self.gameOverFlag == 3:
				self.gameOverFlag = 0
			pygame.display.update()
			pygame.time.delay(10)
			self.gameOverCount += 1
			self.gameOver()
		#pygame.time.delay(3000)

	#do all the drawing
	def Draw(self):

		#self.screen.fill(pygame.Color(255,255,255))
		#self.screen.blit(self.bg1,(0,0))
		self.level.Draw()

		#if player takes damage have him flickr beautifully
		if self.player.invulnDuration > 0:
			self.playerFlip = not self.playerFlip
		else:
			self.playerFlip = True

		if self.playerFlip:
			self.players.draw(self.screen)
		self.level.fg.Draw(self.screen)
		self.drawGUI()


	def drawGUI(self):
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/OSGCC6/images/bean.png"
		img = pygame.image.load(imgPath)
		for i in range(self.player.hp):
			self.screen.blit(img,(40 * (i + 1), 50))			



	def getEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.QUIT
				sys.exit()
		keystate =  pygame.key.get_pressed()
		if keystate:
			self.player.Update(keystate)


	def addPlayer(self, player):
		self.players.add(player)
		self.player = player

	def setLevel(self, level):
		self.level = level


	def addObject(self, object):
		self.objects.add(object)

	def checkCollision(self, obj, newPos):
		return self.level.checkCollision(obj, newPos)