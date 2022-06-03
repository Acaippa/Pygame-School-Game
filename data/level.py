"""
The level module draws and handles some of the logic in the game
"""

import pygame
from data.tile import*
from data.player import*
from data.enemy import*
from data.dialouge import*
from data.items import*
from data.scoreboard import*
import math


class Level:
	"""
	Main level object

	[run]
		fps: int
	"""
	def __init__(self): # initializes the object, this only happens once
		pygame.font.init()
		pygame.mixer.init() # initiating the sound object
		map = [
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
			[1,'p',0,1,'e',0,0,0,0,0,0,0,0,0,0,'e',1,'e',0,0,1,0,0,1],
			[1,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,0,'e',1],
			[1,0,0,1,1,1,1,1,1,0,0,0,0,0,'e','e',0,0,0,0,0,0,0,1],
			[1,0,'x',1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1],
			[1,0,0,1,0,0,'e',0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],
			[1,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1],
			[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1],
			[1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
			[1,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],
			[1,'e',0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,'e',1,0,0,1],
			[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
			]

		# get the dispaly surface for the game
		self.display_surface = pygame.display.get_surface()
		self.display_list = []
		self.obsticle_list = []
		self.enemy_list = []
		self.item_list = []

		#listing all the dialouge counters
		self.noKeyCounter = 0
		self.KeyPickedUp = 0
		self.healthPickedUp = 0

		# defining all the paths for the images
		self.treasure = "images/misc/treasure.png"
		self.bush = "images/background/bush.png"
		self.key = "images/misc/key.png"
		self.health = "images/misc/health.png"

		# loading the background and rescaling the image
		self.background = pygame.image.load('images/background/ground.png').convert()
		self.background = pygame.transform.scale(self.background, (30, 30))
		self.background_rect = self.background.get_rect() 
		self.w, self.h = self.background.get_size()

		# this variable will be used to control the game state in the main game loop
		self.game = True
		self.won = False

		# loading the sounds
		self.explosion = pygame.mixer.Sound('audio/explosion.mp3')
		self.healing = pygame.mixer.Sound('audio/healing.mp3')

		self.explosion.set_volume(0.5)
		self.healing.set_volume(0.5)

		for row_index, row in enumerate(map): # loops through the rows and collumns in the map variable above
			for col_index, col in enumerate(row):
				x = col_index*50
				y = row_index*50
				if col == 1: # check if the tile should be a bush
					self.obsticle_list.append(Tile((x, y), self.bush))
					self.display_list.append(Tile((x, y), self.bush))

				if col == 'p': # player
					self.player = Player([x,y], self.obsticle_list, self.enemy_list)

				if col == 'e': # enemy
					self.enemy_list.append(Enemy([x, y], self.player, self.obsticle_list))

				if col == 'x': # treasure
					self.display_list.append(Tile((x, y), self.treasure))
					self.obsticle_list.append(Tile((x, y), self.treasure))
					self.treasure = Tile((x, y), self.treasure)

	def run(self, fps): # this is the function that will be run in the main game loop
		self.fps = str(int(fps))
		pygame.display.set_mode((1500, 600))

		# draws the grass blocks using a nested for loop
		for x in range(1200//self.w):
			for y in range(600//self.h+1):
				self.display_surface.blit(self.background, (x*self.w, y*self.h))

		for i in self.display_list:
			i.draw()

		for i in self.item_list:
			if i.picked_up == False:
				i.update()
			else:
				self.item_list.remove(i)
				if i.id == "key":
					self.KeyPickedUp = 40
				if i.id == "health":
					pygame.mixer.Sound.play(self.healing)
					self.healthPickedUp = 40

		# draws the enemies if they are alive, and if they're dead, play the epic explosion sound
		for i in self.enemy_list:
			if i.living:
				i.draw()
			else:
				self.enemy_list.remove(i)
				pygame.mixer.Sound.play(self.explosion)
				# this function handles the drop logics
				self.item_drop(i)


		# initiating the fps font and blitting it in the topleft corner of the screen
		self.fps_font = pygame.font.SysFont("Sans", 30)
		self.fps_font = self.fps_font.render(self.fps, True, '#ffffff')
		self.display_surface.blit(self.fps_font, (0,0))


		dialouge = Dialouge() # creating an instance of the dialouge class

		dst = math.hypot(self.player.rect.x - self.treasure.pos[0], self.player.rect.y - self.treasure.pos[1])
		if dst <= 50:
			dialouge.text = "Press E to open"
			if self.player.action:
				self.noKeyCounter = 100

		# checking if the player is alive
		if self.player.living == False:
			self.game = False
			self.win = False 

		# dialog timers and checks for game finishes
		try:
			if self.noKeyCounter > 0:
				if self.player.has_key == False:
					dialouge.text = "I do not have a key"
				else:
					self.game = False # changes the game variable so the main loop knows that the game is finished
					self.won = True
				self.noKeyCounter -= 1

			# triggers dialouges if certain parameters are true
			elif self.KeyPickedUp > 0:
				dialouge.text = "I picked up a key!"
				self.KeyPickedUp -= 1

			elif self.healthPickedUp > 0:
				dialouge.text = "I gained some health"
				self.healthPickedUp -= 1
		except Exception as e:
			print(e)

		dialouge.draw()

		self.player.update()

		# scoreboard
		scoreboard = ScoreBoard(self.background_rect, self.player, self.enemy_list)
		scoreboard.draw()

	def item_drop(self, enemy): # logic for dropping items
		amount_of_enemies = len(self.enemy_list)
		enemy = enemy # the enemy that triggered this function

		if amount_of_enemies == 0: # if the last turret is killed, the key wil drop
			self.item_list.append(Item(enemy.pos, self.key, self.player, "key"))

		self.item_list.append(Item(enemy.pos, self.health, self.player, "health"))

	def idle(self): # this is the idle state used when the menu overlaps the game
		for i in self.display_list:
			i.draw()
