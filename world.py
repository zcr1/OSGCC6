import pygame


class World():
	size = width, height = 1600, 900
	gravity = .8
	def __init__(self):
		self.screen = pygame.display.set_mode(self.size)
		self.objects = pygame.sprite.Group() #hold random objects/sprites
		self.players = pygame.sprite.Group()
		self.player = None
		self.enemy = pygame.sprite.Group()
		self.clock = pygame.time.Clock()

	#gets called by main game loop to do everything
	def Update(self):
		self.getEvents()
		self.Draw()
		for obj in self.objects:
			if not obj.Update():
				obj.kill()


	#do all the drawing
	def Draw(self):
		self.screen.fill(pygame.Color(255,255,255))
		self.level.Draw()
		self.players.draw(self.screen)
		self.objects.draw(self.screen)
		self.enemy.draw(self.screen)

	def getEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.QUIT
				sys.exit()
		keystate =  pygame.key.get_pressed()
		if keystate:
                        self.enemy.Update(keystate)
			self.player.Update(keystate)


	def addPlayer(self, player):
		self.players.add(player)
		self.player = player

	def setLevel(self, level):
		self.level = level


	def addObject(self, object):
		self.objects.add(object)

	def addEnemy(self, enemy):
                self.enemy.add(enemy)
