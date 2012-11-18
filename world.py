import pygame
import os

class World():
	size = width, height = 1600, 900
	gravity = .3
	def __init__(self):
		self.screen = pygame.display.set_mode(self.size)
		self.objects = pygame.sprite.Group() #hold random objects/sprites
		self.players = pygame.sprite.Group()
		self.player = None
		self.clock = pygame.time.Clock()
		bgPath1 = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/background1.png"
		bgPath2 = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/background2.png"
		self.bg1 = pygame.image.load(bgPath1).convert()

		self.playerFlip = True

	#gets called by main game loop to do everything
	def Update(self):
		self.getEvents()
		if self.player.dead:
			self.gameOver()
			return

		self.Draw()
		self.level.Update()
		for obj in self.objects:
			if not obj.Update():
				obj.kill()



	def gameOver(self):
		pygame.font.init()
		self.screen.fill(pygame.Color(224,24,13))
		fontobj = pygame.font.Font(None,80)
		msg = fontobj.render("YOU ARE LOSE", 1, (0,0,0))
		self.screen.blit(msg,[700,450], area=None, special_flags=0)

	#do all the drawing
	def Draw(self):

		#self.screen.fill(pygame.Color(255,255,255))
		self.screen.blit(self.bg1,(0,0))
		self.level.Draw()

		#if player takes damage have him flickr beautifully
		if self.player.invulnDuration > 0:
			self.playerFlip = not self.playerFlip
		else:
			self.playerFlip = True

		if self.playerFlip:
			self.players.draw(self.screen)
		self.drawGUI()


	def drawGUI(self):
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/osgcc/images/bean.png"
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